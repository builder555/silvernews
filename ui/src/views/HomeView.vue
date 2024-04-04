<script setup>
const stories = [
  {id: 1, title: 'test story 1', poster: 'user1', url: 'https://www.google.com'},
  {id: 2, title: 'test story 2', poster: 'user2', content: 'hello there'},
  {id: 3, title: 'test story 3', poster: 'user3', url: 'https://www.yahoo.com'},
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
