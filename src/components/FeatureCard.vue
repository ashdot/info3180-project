<template>
    <div class="feature">
        <div class="icon">
            <span v-html="icon"></span>
        </div>
      <h3>{{ title }}</h3>
      <p>{{ text }}</p>
    </div>
</template>
  
<script setup>
defineProps(['icon', 'title', 'text'])
</script>
  
<style scoped>
.feature {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin: 20px auto 0;
    padding: 0 50px;
}
  
.icon {
    background: linear-gradient(to right, #ff4d4d, #ff7a45);
    padding: 15px;
    border-radius: 50%;
    display: inline-flex;
}
  
.icon img {
    width: 40px;
    height: 40px;
    object-fit: contain;
}

.feature h3 {
    font-size: 18px;
    margin-top: 10px;
    margin-bottom: 8px;
    font-weight: bold;
}

.feature p {
    font-size: 14px;
    color: #666;
    /*max-width: 260px;*/
    line-height: 1.5;
}

/* MOBILE */
@media (max-width: 768px) {
    .feature {
        margin: 20px auto 0;
        padding: 0 100px;
    }
}
</style>