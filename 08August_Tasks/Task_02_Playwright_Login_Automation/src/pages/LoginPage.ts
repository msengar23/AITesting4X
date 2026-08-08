import { type Locator, type Page, expect } from '@playwright/test';

export class LoginPage {
  private readonly emailInput: Locator;
  private readonly passwordInput: Locator;
  private readonly signInButton: Locator;
  private readonly rememberMeCheckbox: Locator;
  private readonly forgotPasswordButton: Locator;
  private readonly googleSignInButton: Locator;
  private readonly ssoSignInButton: Locator;
  private readonly passkeySignInButton: Locator;
  private readonly loginForm: Locator;
  private readonly notificationBox: Locator;

  constructor(readonly page: Page) {
    this.loginForm = page.locator('form#js-login-form');
    this.emailInput = page.locator('input#login-username');
    this.passwordInput = page.locator('input#login-password');
    this.signInButton = page.locator('button#js-login-btn');
    this.rememberMeCheckbox = page.locator('input#checkbox-remember');
    this.forgotPasswordButton = page.locator('form#js-login-form').getByRole('button', { name: 'Forgot Password?' });
    this.googleSignInButton = page.locator('button#js-google-signin-btn');
    this.ssoSignInButton = page.getByRole('button', { name: 'Sign in using SSO' });
    this.passkeySignInButton = page.getByRole('button', { name: 'Sign in with Passkey' });
    this.notificationBox = page.locator('div#js-notification-box.notification-box--warning');
  }

  get emailField(): Locator {
    return this.emailInput;
  }

  get passwordField(): Locator {
    return this.passwordInput;
  }

  get signInBtn(): Locator {
    return this.signInButton;
  }

  get rememberMe(): Locator {
    return this.rememberMeCheckbox;
  }

  async navigate(): Promise<void> {
    await this.page.goto('/#/login');
    await expect(this.loginForm).toBeVisible();
  }

  async fillEmail(email: string): Promise<void> {
    await this.emailInput.fill(email);
  }

  async fillPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
  }

  async fillCredentials(email: string, password: string): Promise<void> {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
  }

  async clickSignIn(): Promise<void> {
    await this.signInButton.click();
  }

  async login(email: string, password: string): Promise<void> {
    await this.fillCredentials(email, password);
    await this.clickSignIn();
  }

  async checkRememberMe(): Promise<void> {
    const checkbox = this.rememberMeCheckbox;
    if (!(await checkbox.isChecked())) {
      await this.page.getByText('Remember me', { exact: true }).click();
    }
  }

  async uncheckRememberMe(): Promise<void> {
    const checkbox = this.rememberMeCheckbox;
    if (await checkbox.isChecked()) {
      await checkbox.uncheck({ force: true });
    }
  }

  async clickForgotPassword(): Promise<void> {
    await this.forgotPasswordButton.click();
  }

  async clickGoogleSignIn(): Promise<void> {
    await this.googleSignInButton.click();
  }

  async clickSsoSignIn(): Promise<void> {
    await this.ssoSignInButton.click();
  }

  async clickPasskeySignIn(): Promise<void> {
    await this.passkeySignInButton.click();
  }

  async isLoginFormVisible(): Promise<boolean> {
    return this.loginForm.isVisible();
  }

  async isEmailVisible(): Promise<boolean> {
    return this.emailInput.isVisible();
  }

  async isPasswordVisible(): Promise<boolean> {
    return this.passwordInput.isVisible();
  }

  async getInvalidCredentialsError(): Promise<string> {
    await expect(this.notificationBox).toBeVisible();
    return (await this.notificationBox.textContent()) ?? '';
  }

  async waitForInvalidCredentialsError(): Promise<string> {
    await this.notificationBox.waitFor({ state: 'visible' });
    return (await this.notificationBox.textContent()) ?? '';
  }

  async expectInvalidCredentialsError(message: string): Promise<void> {
    await expect(this.notificationBox).toContainText(message);
  }

  async getPageUrl(): Promise<string> {
    return this.page.url();
  }

  async getPageTitle(): Promise<string> {
    return this.page.title();
  }
}
