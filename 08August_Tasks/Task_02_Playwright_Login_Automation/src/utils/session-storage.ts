import { type Page } from '@playwright/test';
import { env } from './env-config';

const SESSION_KEY = 'wingify.test.credentials';

export interface Credentials {
  username: string;
  password: string;
}

async function ensureAppOrigin(page: Page): Promise<void> {
  const url = page.url();
  if (!url.startsWith(env.baseUrl)) {
    await page.goto(`${env.baseUrl}/#/login`, { waitUntil: 'domcontentloaded' });
  }
}

export async function seedCredentials(page: Page): Promise<Credentials> {
  const credentials: Credentials = {
    username: env.validUsername,
    password: env.validPassword,
  };
  await ensureAppOrigin(page);
  await page.evaluate(([key, value]) => {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  }, [SESSION_KEY, credentials] as const);
  return credentials;
}

export async function readCredentials(page: Page): Promise<Credentials> {
  const stored = await page.evaluate((key) => window.sessionStorage.getItem(key), SESSION_KEY);
  if (!stored) {
    throw new Error(`No credentials found in sessionStorage under key "${SESSION_KEY}". Seed them with seedCredentials(page) first.`);
  }
  return JSON.parse(stored) as Credentials;
}

export async function seedInvalidCredentials(page: Page): Promise<Credentials> {
  const credentials: Credentials = {
    username: env.invalidUsername,
    password: env.invalidPassword,
  };
  await ensureAppOrigin(page);
  await page.evaluate(([key, value]) => {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  }, [SESSION_KEY, credentials] as const);
  return credentials;
}
