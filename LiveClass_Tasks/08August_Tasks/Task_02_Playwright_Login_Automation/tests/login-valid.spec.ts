import { test, expect } from '../src/fixtures/fixtures';

test.describe('Wingify Login - Valid Credentials', () => {
  test('should display the login form with all required elements', async ({ pageFactory }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await expect(loginPage.isLoginFormVisible()).resolves.toBe(true);
    await expect(loginPage.isEmailVisible()).resolves.toBe(true);
    await expect(loginPage.isPasswordVisible()).resolves.toBe(true);
    await expect(loginPage.getPageTitle()).resolves.toBe('Login - Wingify');
  });

  test('should keep the sign-in button enabled for a valid email and password', async ({ pageFactory, credentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await loginPage.fillCredentials(credentials.username, credentials.password);
    await expect(loginPage.signInBtn).toBeEnabled();
  });

  test('should remember the email when remember me is checked', async ({ pageFactory, credentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await loginPage.fillEmail(credentials.username);
    await loginPage.checkRememberMe();
    await expect(loginPage.rememberMe).toBeChecked();
    await expect(loginPage.emailField).toHaveValue(credentials.username);
  });

  test('should keep the remember me checkbox unchecked by default', async ({ pageFactory }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await expect(loginPage.rememberMe).not.toBeChecked();
  });

  test('should reveal and hide the password via the visibility toggle', async ({ pageFactory, credentials }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await loginPage.fillPassword(credentials.password);
    await expect(loginPage.passwordField).toHaveAttribute('type', 'password');
    await loginPage.page.getByRole('button', { name: 'Toggle password visibility' }).click();
    await expect(loginPage.passwordField).toHaveAttribute('type', 'text');
  });

  test('should show the forgot password form when forgot password is clicked', async ({ pageFactory }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await loginPage.clickForgotPassword();
    await expect(loginPage.page.locator('form#js-forgot-password-form')).toBeVisible();
  });

  test('should navigate to the Google sign-in flow when the Google button is clicked', async ({ pageFactory }) => {
    const loginPage = pageFactory.loginPage;
    await loginPage.navigate();
    await loginPage.clickGoogleSignIn();
    await loginPage.page.waitForURL(/accounts\.google\.com/, { timeout: 30_000 });
  });
});
