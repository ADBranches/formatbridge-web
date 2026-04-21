const TOKEN_KEY = "formatbridge_auth_token";
const USER_KEY = "formatbridge_auth_user";

function readJson(key) {
  const rawValue = window.localStorage.getItem(key);
  if (!rawValue) return null;

  try {
    return JSON.parse(rawValue);
  } catch {
    return null;
  }
}

const authStore = {
  getToken() {
    return window.localStorage.getItem(TOKEN_KEY) || "";
  },

  getUser() {
    return readJson(USER_KEY);
  },

  isAuthenticated() {
    return Boolean(this.getToken());
  },

  setSession({ token, user }) {
    window.localStorage.setItem(TOKEN_KEY, token);
    window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  },

  clearSession() {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_KEY);
  },
};

export default authStore;