<template>
  <header class="header">
    <div class="left">
      <div class="logo-circle">❤</div>
      <span class="logo-text">DriftDater</span>
    </div>

    <div class="right">
      <!-- LOGIN -->
      <RouterLink 
        to="/login" 
        class="nav-btn"
        :class="{ active: $route.path === '/login' }"
      >
        Login
      </RouterLink>

      <!-- SIGNUP -->
      <RouterLink 
        to="/signup" 
        class="nav-btn"
        :class="{ active: $route.path === '/signup' }"
      >
        Sign Up
      </RouterLink>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 15px 40px;
  background: #f3f3f5;

  position: sticky;
  top: 0;
  z-index: 1000; /* 🔥 fixes overlap issue */

  border-bottom: 1px solid #e5e5e5;
}

.left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-circle {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  display: flex;
  align-items: center;
  justify-content: center;

  color: white;
  font-size: 18px;
}

.logo-text {
  font-size: 22px;
  font-weight: bold;
  color: #ff4d79;
}

.right {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 🔥 SHARED BUTTON STYLE */
.nav-btn {
  padding: 8px 18px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* 🔥 DEFAULT (outlined look) */
.nav-btn {
  background: white;
  border: 2px solid #ff6a5c;
  color: #ff6a5c;
}

/* 🔥 ACTIVE (filled gradient) */
.nav-btn.active {
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  color: white;
  border: none;
}
</style>