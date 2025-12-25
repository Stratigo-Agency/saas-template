<script setup lang="ts">
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'
import { useRouter, RouterLink } from 'vue-router'
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Home, Inbox, User, LogOut } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

const router = useRouter()
const authStore = useAuthStore()

// Define the type for menu items
interface MenuItem {
  title: string
  route: string
  icon: any
  requiresAuth?: boolean
}

// Menu items
const items: MenuItem[] = [
  {
    title: 'Dashboard',
    route: '/dashboard',
    icon: Home
  },
  {
    title: 'Inbox',
    route: '/inbox',
    icon: Inbox,
    requiresAuth: true
  },
]

const filteredItems = computed(() => {
  return items.filter(item => !item.requiresAuth || authStore.isAuthenticated)
})

const navigateTo = (route: string) => {
  router.push(route)
}

const handleSignOut = async () => {
  const { success } = await authStore.signOut()
  if (success) {
    router.push('/login')
  }
}

const goToProfile = () => {
  router.push('/profile')
}
</script>

<template>
  <nav class="w-full border-b bg-background">
    <div class="mx-auto px-12 py-3 flex items-center justify-between">
      <!-- Logo/Brand -->
      <div class="flex items-center space-x-8">
        <h1 class="text-xl font-bold">Saas Starter</h1>
        
        <!-- Navigation Menu -->
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem v-for="item in filteredItems" :key="item.title">
              <NavigationMenuLink 
                as-child
                :class="navigationMenuTriggerStyle()"
              >
                <RouterLink :to="item.route" class="flex items-center">
                  <component :is="item.icon" class="mr-2 h-4 w-4" />
                  {{ item.title }}
                </RouterLink>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>

      <!-- User Profile & Actions -->
      <div v-if="authStore.isAuthenticated" class="flex items-center space-x-4">
        <!-- User Info -->
        <div 
          class="flex items-center space-x-2 cursor-pointer hover:bg-muted/50 px-3 py-2 rounded-md transition-colors"
          @click="goToProfile"
        >
          <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
            <User class="w-4 h-4" />
          </div>
          <div class="hidden md:block">
            <p class="text-sm font-medium">{{ authStore.user?.email }}</p>
            <p class="text-xs text-muted-foreground">
              {{ authStore.user?.user_metadata?.full_name || 'User' }}
            </p>
          </div>
        </div>
        
        <!-- Sign Out Button -->
        <Button 
          variant="outline"
          @click="handleSignOut"
          class="flex items-center"
        >
          <LogOut class="mr-2 h-4 w-4" />
          <span class="hidden sm:inline">Sign Out</span>
        </Button>
      </div>
      
      <!-- Not Authenticated (shouldn't show in app view, but just in case) -->
      <div v-else class="flex items-center space-x-2">
        <Button variant="ghost" @click="navigateTo('/login')">
          Sign In
        </Button>
        <Button @click="navigateTo('/register')">
          Sign Up
        </Button>
      </div>
    </div>
  </nav>
</template>

