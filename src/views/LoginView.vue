<template>
  <div class="page">
    <div class="card">
      
      <div class="logo">
        <img src="@/assets/logo.png" alt="DriftDater Logo" />
      </div>

      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to continue your journey</p>

      <!-- ERROR -->
      <div
        v-if="errorMessage"
        class="error-box"
      >
        {{ errorMessage }}
      </div>

      <!-- LOGIN FORM -->
      <form @submit.prevent="handleLogin">

        <label>Email Address</label>
        <div class="input-box">
          <input 
            type="email" 
            placeholder="you@example.com" 
            v-model="email" 
            required
          />
        </div>

        <label>Password</label>
        <div class="input-box">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            placeholder="Enter your password" 
            v-model="password" 
            required
          />

          <button type="button" class="toggle" @click="showPassword = !showPassword">
            {{ showPassword ? 'Hide' : 'Show' }}
          </button>
        </div>

        <div class="row">
          <label class="remember">
            <input type="checkbox" v-model="remember" />
            Remember me
          </label>

          <!--probably remove this-->
          <a href="#" class="forgot">Forgot password?</a>
        </div>

        <!--<button class="btn">Login</button>-->
        <!-- SUBMIT -->
        <button
          class="btn"
          :disabled="loading"
        >

          <span v-if="loading">
            Logging in...
          </span>

          <span v-else>
            Login
          </span>

        </button>
      </form>

      <p class="bottom">
        Don't have an account? 
        <span @click="$router.push('/signup')">Sign up</span>
      </p>

    </div>
  </div>
</template>

<script setup>

/*export default {
  data() {
    return {
      email: "",
      password: "",
      remember: false,
      showPassword: false
    };
  },
  methods: {
    handleLogin() {
      console.log(this.email, this.password);
    }
  }
};*/

import { ref } from 'vue'
import { useRouter } from 'vue-router'

import api from '@/services/api'

const router = useRouter()

// FORM DATA
const email = ref('')
const password = ref('')

const remember = ref(false)
const showPassword = ref(false)

// UI STATES
const loading = ref(false)
const errorMessage = ref('')

// LOGIN
const handleLogin = async () => {

  errorMessage.value = ''

  // VALIDATION
  if (!email.value || !password.value) {

    errorMessage.value =
      'Please enter your email and password.'

    return
  }

  loading.value = true

  try {

    // BACKEND REQUEST
    const response = await api.post(
      '/auth/login',
      {
        email: email.value,
        password: password.value
      }
    )

    // USER DATA
    const user = response.data.user

    // STORE SESSION DATA
    localStorage.setItem(
      'user_id',
      user.user_id
    )

    localStorage.setItem(
      'username',
      user.username
    )

    localStorage.setItem(
      'isLoggedIn',
      'true'
    )

    // OPTIONAL TOKEN SUPPORT
    // Only if backend later returns token
    if (response.data.token) {

      localStorage.setItem(
        'token',
        response.data.token
      )
    } else {

      // Temporary fallback
      localStorage.setItem(
        'token',
        'logged_in'
      )
    }

    // REDIRECT
    router.push('/discover')

  } catch (error) {

    console.error(error)

    // BACKEND ERROR MESSAGE
    if (error.response?.data?.error) {

      errorMessage.value =
        error.response.data.error

    } else {

      errorMessage.value =
        'Something went wrong. Please try again.'
    }

  } finally {

    loading.value = false

  }
}

</script>

<style scoped>

.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f7;
  padding: 40px 0;
}

.card {
  width: 550px;
  background: white;
  padding: 40px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.logo img {
  width: 70px;
  height: 70px;
  object-fit: contain;
}

.subtitle {
  color: gray;
  margin-bottom: 20px;
}

label {
  display: block;
  text-align: left;
  margin-top: 15px;
  font-weight: 500;
}

.input-box {
  position: relative;
  margin-top: 5px;
}

.input-box input {
  width: 100%;
  padding: 12px 70px 12px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

/* remove browser eye */
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
  display: none;
}

.toggle {
  position: absolute;
  right: 10px;
  top: 8px;
  background: none;
  border: none;
  color: #ff4d79;
  font-size: 13px;
  cursor: pointer;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  font-size: 14px;
}

.remember {
  display: flex;
  align-items: center;
  gap: 6px;
}

.forgot {
  color: #ff4d79;
  text-decoration: none;
}

.btn {
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.bottom {
  margin-top: 20px;
}

.bottom span {
  color: #ff4d79;
  cursor: pointer;
}
</style>