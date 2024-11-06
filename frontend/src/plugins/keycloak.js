import Keycloak from 'keycloak-js';

const keycloakConfig = {
  url: 'http://172.16.1.158:8080', // Replace with your Keycloak server URL
  realm: 'aastha-omega',
  clientId: 'oemga'
};

const keycloak = new Keycloak(keycloakConfig);

export const initializeKeycloak = (onAuthenticatedCallback) => {
  keycloak
    .init({ onLoad: 'login-required', checkLoginIframe: false })
    .then((authenticated) => {
      if (authenticated) {
        console.log("User successfully authenticated.");

        // Set expiration time (assuming token expiration in milliseconds)
        const expireTime = new Date().getTime() + keycloak.tokenParsed.exp * 1000;

        // Store userInfo with value and expire keys
        const userInfo = {
          value: {
            id: keycloak.tokenParsed.sub,
            userName: keycloak.tokenParsed.preferred_username,
            nickname: keycloak.tokenParsed.name || "Nickname",
            email: keycloak.tokenParsed.email || "N/A",
            roles: keycloak.tokenParsed.realm_access.roles || []
          },
          expire: expireTime
        };
        console.log ('userinfo',userInfo)
        localStorage.setItem("userInfo", JSON.stringify(userInfo));

        // Store accessToken with value and expire keys
        const accessToken = {
          value: keycloak.token,
          expire: expireTime
        };
        console.log('accesstoken',accessToken)
        localStorage.setItem("accessToken", JSON.stringify(accessToken));

        // Store refreshToken with value and expire keys
        const refreshToken = {
          value: keycloak.refreshToken,
          expire: expireTime
        };
        localStorage.setItem("refreshToken", JSON.stringify(refreshToken));

        // Callback on successful authentication
        onAuthenticatedCallback();
      } else {
        console.warn("User not authenticated; reloading page for login.");
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Keycloak authentication failed:", error);
    });
};

export default keycloak;
