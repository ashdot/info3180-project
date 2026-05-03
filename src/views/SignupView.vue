<template>
  <div class="page">
    <div class="card">

      <div class="logo-circle">❤</div>

      <h1>Create Your Profile</h1>
      <p class="subtitle">Join thousands of singles looking for love</p>

      <!-- UPLOAD -->
      <div class="upload-box" @click="triggerFile">
        <input type="file" ref="fileInput" hidden @change="handleFile" />

        <div class="upload-circle">
          <img v-if="preview" :src="preview" />
          <span v-else>Upload</span>
        </div>

        <p class="upload-text">Upload Profile Photo</p>
      </div>

      <form @submit.prevent="handleSignup">

        <div class="row">
          <div class="field">
            <label>Full Name *</label>
            <input type="text" placeholder="John Doe" v-model="name" />
          </div>

          <div class="field">
            <label>Age *</label>
            <input type="number" placeholder="25" v-model="age" />
          </div>
        </div>

        <div class="field">
          <label>Email *</label>
          <input type="email" placeholder="you@example.com" v-model="email" />
        </div>

        <div class="field">
          <label>Location *</label>
          <input type="text" placeholder="Kingston, Jamaica" v-model="location" />
        </div>

        <div class="row">
          <div class="field">
            <label>Gender *</label>
            <select v-model="gender">
              <option disabled value="">Select gender</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          <div class="field">
            <label>Looking For *</label>
            <select v-model="lookingFor">
              <option disabled value="">Select preference</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>
        </div>

        <!-- PASSWORD -->
        <div class="row">
          <div class="field">
            <label>Password *</label>
            <div class="input-box">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                v-model="password"
                placeholder="Enter password"
              />
              <button 
                type="button" 
                class="toggle"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <div class="field">
            <label>Confirm Password *</label>
            <div class="input-box">
              <input 
                :type="showConfirm ? 'text' : 'password'" 
                v-model="confirmPassword"
                placeholder="Confirm password"
              />
              <button 
                type="button" 
                class="toggle"
                @click="showConfirm = !showConfirm"
              >
                {{ showConfirm ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>
        </div>

        <!-- TERMS -->
        <div class="terms">
    <input type="checkbox" v-model="agree" />
    <p>
        I agree to the 
        <span>Terms of Service</span> and 
        <span>Privacy Policy</span>.
    </p>
    </div>

        <button class="btn">Create Account</button>

      </form>

      <p class="bottom">
        Already have an account? 
        <span @click="$router.push('/login')">Login</span>
      </p>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      age: "",
      email: "",
      location: "",
      gender: "",
      lookingFor: "",
      password: "",
      confirmPassword: "",
      agree: false,
      preview: null,

      // 🔥 REQUIRED for toggle
      showPassword: false,
      showConfirm: false
    };
  },
  methods: {
    triggerFile() {
      this.$refs.fileInput.click();
    },
    handleFile(e) {
      const file = e.target.files[0];
      if (file) {
        this.preview = URL.createObjectURL(file);
      }
    },
    handleSignup() {
      console.log("Signup submitted");
    }
  }
};
</script>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
  background: #f5f5f7;
}

.card {
  width: 550px;
  background: white;
  padding: 35px;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  text-align: center;
}

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
}

.subtitle {
  color: gray;
  margin-bottom: 20px;
}

.row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.field {
  flex: 1;
  text-align: left;
  margin-top: 15px;
}

input, select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

input::placeholder {
  color: #aaa;
}

/* REMOVE BROWSER EYE */
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
  display: none;
}

/* PASSWORD BOX */
.input-box {
  position: relative;
}

.input-box input {
  padding: 12px 70px 12px 12px;
}

/* SHOW/HIDE BUTTON */
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

/* UPLOAD */
.upload-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: auto;
  overflow: hidden;
}

.upload-circle img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-text {
  color: #ff4d79;
}

/* TERMS FIXED */
.terms {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 15px;
  font-size: 14px;
}

.terms p {
  margin: 0;
  line-height: 1.5;
  text-align: left;
}

.terms span {
  color: #ff4d79;
  cursor: pointer;
  font-weight: 500;
}

/* BUTTON */
.btn {
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #ff4d79, #ff6a5c);
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.bottom span {
  color: #ff4d79;
  cursor: pointer;
}
</style>