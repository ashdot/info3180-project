<template>
  <div class="page">

    <div class="card">

      <div class="logo">
        <img src="@/assets/logo.png" alt="DriftDater Logo" />
      </div>

      <h1>Create Account</h1>

      <p class="subtitle">
        Join DriftDater today
      </p>

      <form @submit.prevent="handleSignup">

        <!-- FIRST + LAST -->
        <div class="row">

          <div class="field">
            <label>First Name *</label>

            <input
              type="text"
              placeholder="John"
              v-model="first_name"
            />
          </div>

          <div class="field">
            <label>Last Name *</label>

            <input
              type="text"
              placeholder="Doe"
              v-model="last_name"
            />
          </div>

        </div>

        <!-- USERNAME -->
        <div class="field">

          <label>Username *</label>

          <input
            type="text"
            placeholder="johndoe"
            v-model="username"
          />
        </div>

        <!-- EMAIL -->
        <div class="field">

          <label>Email *</label>

          <input
            type="email"
            placeholder="john@email.com"
            v-model="email"
          />
        </div>

        <!-- DOB -->
        <div class="field">

          <label>Date of Birth *</label>

          <input
            type="date"
            v-model="dob"
          />
        </div>

        <!-- GENDER + LOOKING FOR -->
        <div class="row">

          <div class="field">

            <label>Gender *</label>

            <select v-model="gender">

              <option value="man">Man</option>
              <option value="woman">Woman</option>
              <option value="other">Other</option>

            </select>
          </div>

          <div class="field">

            <label>Looking For *</label>

            <select v-model="looking_for">

              <option value="long_term">
                Long-term Relationship
              </option>

              <option value="casual">
                Casual / Hookups
              </option>

              <option value="friendship">
                Friendship / Companionship
              </option>

              <option value="flow">
                Going with the Flow
              </option>

            </select>
          </div>

        </div>

        <!-- PASSWORDS -->
        <div class="row">

          <div class="field">

            <label>Password *</label>

            <div class="input-box">

              <input
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter password"
                v-model="password"
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
                placeholder="Confirm password"
                v-model="confirmPassword"
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

          <input
            type="checkbox"
            v-model="agree"
          />

          <p>
            I agree to the
            <span>Terms of Service</span>
            and
            <span>Privacy Policy</span>.
          </p>

        </div>

        <!-- BUTTON -->
        <!--make this redirect to into the actual app-->
        <button class="btn">
          Create Account 
        </button>

      </form>

      <p class="bottom">
        Already have an account?

        <span @click="$router.push('/login')">
          Login
        </span>
      </p>

    </div>

  </div>
</template>

<script>
export default {

  data() {
    return {

      email: "",
      username: "",

      first_name: "",
      last_name: "",

      dob: "",

      gender: "man",
      looking_for: "long_term",

      password: "",
      confirmPassword: "",

      agree: false,

      showPassword: false,
      showConfirm: false
    };
  },

  methods: {

    handleSignup() {

      if (
        !this.first_name ||
        !this.last_name ||
        !this.username ||
        !this.email ||
        !this.dob ||
        !this.password
      ) {
        alert("Please fill in all required fields");
        return;
      }

      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return;
      }

      if (!this.agree) {
        alert("Please agree to the Terms and Conditions");
        return;
      }

      const signupData = {

        email: this.email,
        username: this.username,

        first_name: this.first_name,
        last_name: this.last_name,

        dob: this.dob,

        gender: this.gender,
        looking_for: this.looking_for,

        password: this.password
      };

      console.log(signupData);

      alert("Account Created!");

      this.$router.push({ name: 'search' });
    }
  }
};
</script>

<style scoped>

.page {
  min-height: 100vh;
  background: #f5f5f7;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 40px 20px;
}

.card {
  width: 100%;
  max-width: 600px;

  background: white;

  padding: 35px;

  border-radius: 20px;

  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

.logo {
  text-align: center;
  margin-bottom: 15px;
}

.logo img {
  width: 75px;
  height: 75px;
  object-fit: contain;
}

h1 {
  text-align: center;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: gray;
  margin-bottom: 25px;
}

.row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.field {
  flex: 1;
  margin-top: 15px;
}

.field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

input,
select {
  width: 100%;
  padding: 12px;

  border-radius: 10px;
  border: 1px solid #ddd;

  box-sizing: border-box;
}

.input-box {
  position: relative;
}

.input-box input {
  padding-right: 70px;
}

.toggle {
  position: absolute;

  right: 10px;
  top: 10px;

  border: none;
  background: none;

  color: #ff4d79;

  cursor: pointer;
  font-weight: 600;
}

.terms {
  display: flex;
  gap: 10px;

  margin-top: 20px;
}

.terms input {
  width: auto;
}

.terms p {
  margin: 0;
  font-size: 14px;
}

.terms span {
  color: #ff4d79;
  font-weight: 600;
}

.btn {
  width: 100%;

  margin-top: 25px;

  padding: 14px;

  border: none;
  border-radius: 10px;

  background: linear-gradient(135deg, #ff4d79, #ff6a5c);

  color: white;

  font-weight: bold;

  cursor: pointer;
}

.bottom {
  text-align: center;
  margin-top: 20px;
}

.bottom span {
  color: #ff4d79;
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 700px) {

  .row {
    flex-direction: column;
    gap: 0;
  }
}
</style>