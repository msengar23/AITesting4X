import { config as loadEnv } from 'dotenv';
import path from 'node:path';

loadEnv({ path: path.resolve(process.cwd(), '.env'), override: true });

export const env = {
  baseUrl: get('BASE_URL', 'https://app.wingify.com'),
  validUsername: get('VALID_USERNAME', ''),
  validPassword: get('VALID_PASSWORD', ''),
  invalidUsername: get('INVALID_USERNAME', ''),
  invalidPassword: get('INVALID_PASSWORD', ''),
  invalidCredentialsMessage: get('INVALID_CREDENTIALS_MESSAGE', ''),
  forgotPasswordEmail: get('FORGOT_PASSWORD_EMAIL', ''),
  isCi: get('CI', 'false') === 'true',
  headless: get('HEADLESS', 'true') === 'true',
  reporter: get('REPORTER', 'allure'),
} as const;

function get(key: string, fallback: string): string {
  return process.env[key] ?? fallback;
}
