<template>
  <div class="page">
    <div class="card">
      
      <!--<div class="logo-circle">❤</div>-->
      <div class="logo">
        <img src="@/assets/logo.png" alt="DriftDater Logo" />
      </div>

      <h1>Welcome Back</h1>
      <p class="subtitle">Sign in to continue your journey</p>

      <form @submit.prevent="handleLogin">

        <label>Email Address</label>
        <div class="input-box">
          <input 
            type="email" 
            placeholder="you@example.com" 
            v-model="email" 
          />
        </div>

        <label>Password</label>
        <div class="input-box">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            placeholder="Enter your password" 
            v-model="password" 
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

          <a href="#" class="forgot">Forgot password?</a>
        </div>

        <button class="btn">Sign In</button>
      </form>

      <p class="bottom">
        Don't have an account? 
        <span @click="$router.push('/signup')">Sign up</span>
      </p>

    </div>
  </div>
</template>

<script>
export default {
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
};
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

/*
.logo-circle {
  width: 70px;
  height: 70px;
  margin: auto;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
}
*/

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