import Keycloak from "keycloak-js";
import axios from "axios"; // Import axios for HTTP requests
import { BASE_URL , KEYCLOAK_URL} from "/home/ubuntu/omega-code/frontend/api-config.js";

const keycloakConfig = {
  url: `${KEYCLOAK_URL}`, // Replace with your Keycloak server URL
  realm: "nisha-omega",
  clientId: "omega",
};

const keycloak = new Keycloak(keycloakConfig);

export const initializeKeycloak = (onAuthenticatedCallback) => {
  keycloak
    .init({ onLoad: "login-required", checkLoginIframe: false })
    .then((authenticated) => {
      if (authenticated) {
        console.log("User successfully authenticated.");

        // Set expiration time (assuming token expiration in milliseconds)
        const expireTime =
          new Date().getTime() + keycloak.tokenParsed.exp * 1000;

        // Store userInfo with value and expire keys
        const userInfo = {
          // value: {
          id: keycloak.tokenParsed.sub,
          userName: keycloak.tokenParsed.preferred_username,
          nickname: keycloak.tokenParsed.name || "Nickname",
          email: keycloak.tokenParsed.email || "N/A",
          roles: keycloak.tokenParsed.realm_access.roles || [],
          // },
          // expire: expireTime
        };
        console.log("userinfo", userInfo);
        localStorage.setItem("userInfo", JSON.stringify(userInfo));

        // Store accessToken with value and expire keys
        const accessToken = {
          value: keycloak.token,
          expire: expireTime,
        };
        console.log("accesstoken", accessToken);
        localStorage.setItem("accessToken", JSON.stringify(accessToken));

        // Store refreshToken with value and expire keys
        const refreshToken = {
          value: keycloak.refreshToken,
          expire: expireTime,
        };
        localStorage.setItem("refreshToken", JSON.stringify(refreshToken));


        // Combine userInfo and accessToken into a single object
        const payload = {
          A1: userInfo, // user data
          A2: accessToken, // token data as an object
        };

        // Send user data to Django backend to save or update the user
        axios
          .post(`${BASE_URL}/api/v1/save-keycloak-user/`, payload, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            console.log("User information stored:", response.data);
            onAuthenticatedCallback();
          })
          .catch((error) => {
            console.error("Error during API request:", error.response || error);
          });

      } else {
        console.warn("User not authenticated; reloading page for login.");
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Keycloak authentication failed:", error);
    });
};

export function useKeycloak() {
  return keycloak;
}

// Logout function to log the user out from both the application and Keycloak
export function logoutUser() {
  keycloak.logout({
    redirectUri: `${BASE_URL}`, // Redirect the user to this URL after logout
  });
}

// Example function to call the logoutUser function from your UI
export function handleUserLogout() {
  logoutUser();
}

export default keycloak;
