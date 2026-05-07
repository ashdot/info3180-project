<template>
  <!--also this should only show if the userr isnt logged in-->
  <header v-if="showHeader" class="header">

    <!--make this navigate to home when clicked-->
    <RouterLink to="/" class="logo">
      <img src="@/assets/logo.png" alt="DriftDater Logo" />
      <span class="logo-text">DriftDater</span>
    </RouterLink>

    <div class="buttons">
      <!-- SIGNUP -->
      <RouterLink 
        to="/signup" 
        class="nav-btn-filled"
        :class="{ active: route.path === '/signup' }"
      >
        Sign Up
      </RouterLink>

      <!-- LOGIN -->
      <RouterLink 
        to="/login" 
        class="nav-btn-outline"
        :class="{ active: route.path === '/login' }"
      >
        Login
      </RouterLink>
    </div>
  </header>
</template>

<script setup>
//import { RouterLink } from "vue-router";

import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const isLoggedIn = computed(() => {
  return !!localStorage.getItem("token");
});

const allowedRoutes = ["/", "/login", "/signup"];

const showHeader = computed(() => {
  return !isLoggedIn.value && allowedRoutes.includes(route.path);
});

</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  /*align-items: center;*/

  padding: 15px 40px;
  background: white;

  /*position: sticky;
  top: 0;
  z-index: 1000;   fixes overlap issue */

  border-bottom: 1px solid #e5e5e5;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  cursor: pointer;
}

.logo img {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.logo-text {
  font-weight: 700;
  font-size: 30px;

  background: linear-gradient(to right, #ff4d4d, #ff7a45);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.buttons {
  display: flex;
  align-items: center;
  gap: 0px;
}

.nav-btn-filled{
  margin-left: 10px;
  padding: 8px 40px;
  border-radius: 25px;
  background: linear-gradient(to right, #ff4d4d, #ff7a45);
  color: white;
  border: none;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-btn-outline{
  margin-left: 10px;
  padding: 8px 40px;
  border-radius: 25px;
  border: 2px solid #ff7a45;
  background: transparent;
  text-decoration: none;
  color: #ff7a45;
  font-weight: 500;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .header {
    padding: 5px 20px;
  }

  .logo img {
    width: 26px;
    height: 26px;
  }

  .logo-text {
    font-size: 20px;
  }

  .buttons {
    padding: 3px 14px;
    font-size: 14px;
  }
}
</style>