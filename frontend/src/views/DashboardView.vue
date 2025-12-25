<script setup lang="ts">
import { useSampleHook } from '@/hooks/useSampleHook'
import { onMounted, ref } from 'vue'

const { useSample } = useSampleHook()
const sampleData = ref<any>(null)
const error = ref<string | null>(null)
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const data = await useSample()
    sampleData.value = data
  } catch (err: any) {
    error.value = err.message || 'Failed to load sample data'
    console.error('Error fetching sample data:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
    <p class="mb-4">This is your dashboard page.</p>
    
    <div v-if="loading" class="text-muted-foreground">
      Loading sample data...
    </div>
    
    <div v-else-if="error" class="text-destructive">
      Error: {{ error }}
    </div>
    
    <div v-else-if="sampleData" class="space-y-2">
      <div class="p-4 bg-card rounded-lg border">
        <h2 class="font-semibold mb-2">Sample API Response:</h2>
        <pre class="text-sm overflow-auto">{{ JSON.stringify(sampleData, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

