import { test, expect } from '../src/fixtures/fixtures';
import { env } from '../src/utils/env-config';

test.describe('Wingify Login - Invalid Credentials', () => {
  test.beforeEach(async ({ pageFactory }) => {
    await pageFactory.loginPage.navigate();
  });

  test('should show an error for invalid credentials', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.login(invalidCredentials.username, invalidCredentials.password);
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
  });

  test('should show an error when submitting empty fields', async ({ pageFactory }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.clickSignIn();
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
  });

  test('should show an error when only the email is filled', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.fillEmail(invalidCredentials.username);
    await loginPage.clickSignIn();
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
  });

  test('should show an error when only the password is filled', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.fillPassword(invalidCredentials.password);
    await loginPage.clickSignIn();
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
  });

  test('should not redirect away from the login page after a failed login', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.login(invalidCredentials.username, invalidCredentials.password);
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
    await expect(loginPage.getPageUrl()).resolves.toContain('#/login');
  });

  test('should keep the user on the login page after a failed login', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.login(invalidCredentials.username, invalidCredentials.password);
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
    await expect(loginPage.isLoginFormVisible()).resolves.toBe(true);
  });

  test('should not persist the session after a failed login', async ({ pageFactory, invalidCredentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.login(invalidCredentials.username, invalidCredentials.password);
    await loginPage.expectInvalidCredentialsError(env.invalidCredentialsMessage);
    await expect(loginPage.isLoginFormVisible()).resolves.toBe(true);
  });
});
