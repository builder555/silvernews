<script setup>
const stories = [
  {id: 1, votes: 10, title: 'test story 1', poster: 'user1', url: 'https://www.google.com'},
  {id: 2, votes: 20, title: 'test story 2', poster: 'user2', content: 'hello there'},
  {id: 3, votes: 30, title: 'test story 3', poster: 'user3', url: 'https://www.yahoo.com'},
];
</script>

<template>
  <main>
    <div 
      v-for="story in stories" 
      :key="story.id"
      class="story"
    >{{ story.title }}</div>
  </main>
</template>
<style scoped>
  main {
    padding: 0.5em;
  }
  .story {
    background-color: var(--bg-secondary-color);
    border-radius: 5px;
    margin: 0.3rem;
    padding: 0.3rem;
  }
</style>