import { chromium } from '@playwright/test';
import { env } from '../utils/env-config';

export default async function globalTeardown(): Promise<void> {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  try {
    await page.goto(`${env.baseUrl}/#/login`, { waitUntil: 'domcontentloaded', timeout: 60_000 });
    await page.evaluate(() => {
      window.sessionStorage.clear();
    });
  } finally {
    await browser.close();
  }
}
