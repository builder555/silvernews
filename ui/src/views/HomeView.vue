<script setup>
const stories = [
  {id:1, title: 'test story 1'},
  {id:2, title: 'test story 2'},
  {id:3, title: 'test story 3'},
];
</script>

<template>
  <main>
    <div 
      v-for="story in stories" 
      :key="story.id"
    >{{ story.title }}</div>
  </main>
</template>
