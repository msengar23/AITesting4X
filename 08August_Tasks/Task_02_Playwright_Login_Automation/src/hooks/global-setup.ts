import { chromium } from '@playwright/test';
import { env } from '../utils/env-config';

export default async function globalSetup(): Promise<void> {
  const browser = await chromium.launch({ headless: env.headless });
  const page = await browser.newPage();
  try {
    await page.goto(`${env.baseUrl}/#/login`, { waitUntil: 'domcontentloaded', timeout: 60_000 });
    await page.waitForSelector('form#js-login-form', { timeout: 30_000 });
    await page.evaluate((baseUrl) => {
      window.sessionStorage.setItem('wingify.setup.baseUrl', baseUrl);
    }, env.baseUrl);
  } finally {
    await browser.close();
  }
}
