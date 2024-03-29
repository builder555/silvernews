<script setup>
import { computed } from 'vue';
import { useStore } from '@/stores/theme';
const themeStore = useStore();
const darkIcon = 'https://icongr.am/feather/sun.svg?size=128&color=ffcc00';
const lightIcon = 'https://icongr.am/feather/moon.svg?size=128&color=000';

const themeIcon = computed(() => {
  return themeStore.isDark ? darkIcon : lightIcon;
});
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  themeStore.setDark(true);
}
</script>

<template>
  <header>
    <nav class="nav">
      <div class="nav-left">
        <a class="brand">SilverNews</a>
        <div class="tabs">
          <a>New</a>
          <a>Submit</a>
        </div>
      </div>
      <div class="nav-right">
        <a class="button clear icon-only" @click="themeStore.toggleTheme">
          <img :src="themeIcon" />
        </a>
        <a class="active">Log In</a>
      </div>
    </nav>
  </header>
</template>
