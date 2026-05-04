<template>
      <footer class="footer">
            <p>Copyright &copy {{ year }} Flask Inc.</p>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style scoped>
.footer {
  background: black;
  color: white;
  text-align: center;
  padding: 10px;
  line-height: 1;
}

.footer p {
  margin: 0;
}

</style>