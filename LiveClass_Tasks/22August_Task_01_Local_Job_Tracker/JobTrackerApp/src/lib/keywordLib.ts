import type { AtsResult, KeywordGroup } from '../types'

/**
 * Curated ATS keyword library for modern QA / SDET / Test roles.
 * Used as the default dictionary for the analyzer and insights. It is
 * fully editable at runtime and persisted in IndexedDB.
 */
export const DEFAULT_KEYWORD_GROUPS: KeywordGroup[] = [
  {
    id: 'automation',
    label: 'Test Automation',
    keywords: [
      'selenium', 'playwright', 'cypress', 'webdriverio',
      'test automation', 'automation framework', 'pom', 'page object model',
      'bdd', 'tdd', 'gherkin', 'cucumber', 'testng', 'junit',
      'data driven', 'keyword driven', 'parallel execution', 'flaky tests',
    ],
  },
  {
    id: 'api',
    label: 'API & Integration',
    keywords: [
      'rest', 'restful', 'api testing', 'soap', 'graphql', 'postman',
      'rest assured', 'grpc', 'webhooks', 'contract testing', 'pact',
      'mock', 'vcr', 'wiremock', 'response validation', 'api automation',
    ],
  },
  {
    id: 'languages',
    label: 'Languages & Frameworks',
    keywords: [
      'java', 'python', 'javascript', 'typescript', 'c#', '.net', 'go',
      'ruby', 'kotlin', 'swift', 'node.js', 'flask', 'django', 'spring boot',
      'pytest', 'pyspark', 'scala', 'bash', 'shell scripting',
    ],
  },
  {
    id: 'ci-cd',
    label: 'CI/CD & DevOps',
    keywords: [
      'jenkins', 'github actions', 'gitlab ci', 'azure pipelines', 'circleci',
      'docker', 'kubernetes', 'terraform', 'aws', 'azure', 'gcp',
      'continuous integration', 'continuous delivery', 'infrastructure as code',
      'helm', 'k8s', 'linux', 'vault', 'artifact', 'deployment pipeline',
    ],
  },
  {
    id: 'mobile',
    label: 'Mobile Testing',
    keywords: [
      'appium', 'mobile testing', 'ios', 'android', 'xctest', 'espresso',
      'detox', 'flutter', 'react native', 'device farm', 'emulators', 'simulators',
      'sauce labs', 'browserstack', 'selendroid',
    ],
  },
  {
    id: 'performance',
    label: 'Performance & Load',
    keywords: [
      'jmeter', 'load testing', 'performance testing', 'stress testing',
      'gatling', 'k6', 'locust', 'soak testing', 'spike testing',
      'latency', 'throughput', 'response time', 'profiling', 'bottleneck',
    ],
  },
  {
    id: 'python-data',
    label: 'Data & SQL',
    keywords: [
      'sql', 'sql server', 'mysql', 'postgresql', 'mongodb', 'oracle',
      'etl', 'data validation', 'data migration', 'bigquery', 'redshift',
      'snowflake', 'pandas', 'pyspark', 'hive', 'reporting',
    ],
  },
  {
    id: 'soft',
    label: 'Soft Skills & Process',
    keywords: [
      'agile', 'scrum', 'kanban', 'jira', 'azure devops', 'test plan',
      'test strategy', 'test cases', 'test management', 'test reporting',
      'defect management', 'stakeholder', 'cross-functional', 'mentoring',
      'code review', 'documentation', 'shift left', 'test pyramid',
      'risk based testing', 'regression testing', 'smoke testing', 'uat',
    ],
  },
  {
    id: 'security',
    label: 'Security & Accessibility',
    keywords: [
      'security testing', 'penetration testing', 'owasp', 'oauth2',
      'jwt', 'vulnerability', 'accessibility', 'wcag', 'a11y', 'axe',
      'performance budgets', 'security headers', 'cors',
    ],
  },
]

/** Flatten all keywords to a single lower-cased set for fast lookup. */
export function flattenKeywords(groups: KeywordGroup[]): string[] {
  const set = new Set<string>()
  for (const group of groups) {
    for (const kw of group.keywords) {
      set.add(kw.trim().toLowerCase())
    }
  }
  return Array.from(set)
}

/** Case-insensitive lowercase normalisation used to match raw text. */
function normalise(text: string): string {
  return text.trim().toLowerCase().replace(/\s+/g, ' ')
}

/**
 * Analyse raw job description / resume text against the keyword library.
 * Returns the match score and matched/missing keyword lists.
 */
export function analyseText(text: string, groups: KeywordGroup[]): AtsResult {
  const normalizedText = normalise(text)
  const all = flattenKeywords(groups)
  const totalCount = all.length

  const matched = all.filter((kw) => normalizedText.includes(kw))
  const matchedSet = new Set(matched)
  const missing = all.filter((kw) => !matchedSet.has(kw))

  const score = totalCount > 0 ? Math.round((matched.length / totalCount) * 100) : 0

  return {
    score,
    matched,
    missing,
    foundCount: matched.length,
    totalCount,
  }
}

/**
 * Compute the ATS match score and coverage for a single job based on the
 * keywords that have been marked as covered (job.keywords) versus the full
 * library.
 */
export function jobCoverage(
  covered: string[],
  groups: KeywordGroup[],
): AtsResult {
  const coveredSet = new Set(covered.map((k) => k.trim().toLowerCase()))
  const all = flattenKeywords(groups)
  const totalCount = all.length

  const matched = all.filter((kw) => coveredSet.has(kw))
  const missing = all.filter((kw) => !coveredSet.has(kw))
  const score = totalCount > 0 ? Math.round((matched.length / totalCount) * 100) : 0

  return {
    score,
    matched,
    missing,
    foundCount: matched.length,
    totalCount,
  }
}

/** Human-friendly label for an ATS score band. */
export function scoreBand(score: number): { label: string; tone: 'good' | 'ok' | 'bad' } {
  if (score >= 75) return { label: 'Strong', tone: 'good' }
  if (score >= 45) return { label: 'Needs work', tone: 'ok' }
  return { label: 'Weak', tone: 'bad' }
}