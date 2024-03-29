<script setup>
import { computed } from 'vue';
import { useStore } from '@/stores/theme';
const store = useStore();
const darkIcon = 'https://icongr.am/feather/sun.svg?size=128&color=ffcc00';
const lightIcon = 'https://icongr.am/feather/moon.svg?size=128&color=000';

const themeIcon = computed(() => {
  return store.isDark ? darkIcon : lightIcon;
});
</script>

<template>
  <header>
    <nav class="nav">
      <div class="nav-left">
        <a class="brand">SilverNews</a>
        <div class="tabs">
          <a>New</a>
          <a class="active">Submit</a>
        </div>
      </div>
      <div class="nav-right">
        <a class="button clear icon-only" @click="store.toggleTheme">
          <img :src="themeIcon" />
        </a>
        <a class="active">Log In</a>
      </div>
    </nav>
  </header>
</template>
