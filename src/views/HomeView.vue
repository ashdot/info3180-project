<!--<script setup>
import { ref } from "vue";

let message = ref("Hello World! This is a VueJS and Flask Starter Template.")

</script>

<template>
    <div class="container">
      <div class="text-center">
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        <h1>{{ message }}</h1>
      </div>
    </div>
</template>

<style>
/* Add any component specific styles here */
</style>-->

<template>
  <div>

    <!--<AppHeader />-->

    <!-- LANDING -->
    <section class="landing">
      <div class="content">
        <h1>Find Your Perfect <br><span>Match</span></h1>
        <p>
          Connect with compatible singles in Jamaica. Create your profile,
          discover matches, and start meaningful conversations today!
        </p>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <h2>Why Choose DriftDater?</h2>

      <div class="grid">
        <FeatureCard icon="@/assets/icons/matching.png"
          title="Smart Matching"
          text="Our algorithm finds compatible matches based on your interests, location, and preferences." />

        <FeatureCard icon="@/assets/icons/secure.png"
          title="Safe & Secure"
          text="Your privacy is our priority. All profiles are verified and your data is protected." />

        <FeatureCard icon="@/assets/icons/messaging.png"
          title="Easy Messaging"
          text="Chat with your matches instantly. Start meaningful conversations with ease." />

        <FeatureCard icon="@/assets/icons/connections.png"
          title="Real Connections"
          text="Join thousands of singles looking for genuine relationships and connection." />
      </div>
    </section>

    <!-- CTA -->
    <section class="cta">
      <h2>Ready to Find Love?</h2>
      <p>Join DriftDater today and start your journey</p>
      <button>Create Your Profile Now</button> <!--go back and add functionality-->
    </section>

    <!--<AppFooter />-->

  </div>
</template>

<script setup>
//import AppHeader from '@/components/AppHeader.vue' - was causing it duplicate on the home page
import FeatureCard from '@/components/FeatureCard.vue'
//import AppFooter from '@/components/AppFooter.vue'
</script>

<style scoped>

.landing {
  height: 520px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  background:
    linear-gradient(
      to bottom,
      rgba(255, 77, 77, 0) 0%,       
      rgba(255,122,69,0.55) 80%,    
      rgba(255, 77, 77, 0.85) 100%   
    ),
    url('@/assets/landing.jpg') center/cover no-repeat;
}

.landing h1 {
  font-size: 80px;
  color: white;
  font-weight: 800;
  line-height: 1;
}

.landing span {
  color: #ff3b30;
}

.landing p {
  color: white;
  max-width: 600px;
  line-height: 1.5;
}

.features {
  padding: 60px;
  text-align: center;
}

.features h2{
  font-weight: bold;
  margin-bottom: 40px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 350px);
  justify-content: center;
  gap: 60px 100px;
}

.cta {
  background: linear-gradient(to right, #ff4d4d, #ff7a45);
  text-align: center;
  padding: 60px;
  color: white;
}

.cta h2 {
  font-weight: bold;
}

.cta button {
  background: white;
  color: #ff4d4d;
  padding: 15px 30px;
  border-radius: 30px;
  border: none;
}

/* MOBILE */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }

  .landing h1 {
    font-size: 40px;
  }

  .landing p {
    max-width: 90%;
    font-size: 15px;
    margin: 20px auto 0;
    padding: 0 100px;
  }
}
</style>