<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <AppNavbar />
    <main class="flex-1 p-6">
      <RouterView />
    </main>
  </div>
</template>
