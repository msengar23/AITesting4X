import { test as base, type Page } from '@playwright/test';
import { PageFactory } from '../pages/PageFactory';
import { type Credentials, seedCredentials, seedInvalidCredentials } from '../utils/session-storage';

type Fixtures = {
  pageFactory: PageFactory;
  credentials: Credentials;
  invalidCredentials: Credentials;
};

export const test = base.extend<Fixtures>({
  pageFactory: async ({ page }, use) => {
    const factory = new PageFactory(page);
    await use(factory);
  },
  credentials: async ({ page }, use) => {
    await use(await seedCredentials(page));
  },
  invalidCredentials: async ({ page }, use) => {
    await use(await seedInvalidCredentials(page));
  },
});

export { expect } from '@playwright/test';
export type { Page };
