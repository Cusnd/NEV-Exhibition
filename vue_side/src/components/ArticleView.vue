<template>
  <div class="container mt-5 pt-4">
    <div class="article-container" v-if="article">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><router-link to="/">首页</router-link></li>
          <li class="breadcrumb-item active">{{ article.car_name }}</li>
        </ol>
      </nav>

      <div class="card">
        <div class="card-body">
          <h1 class="card-title">{{ article.title }}</h1>
          <div class="text-muted mb-4">
            发布时间：{{ formatTime(article.created_at) }}
          </div>
          <div class="article-content" v-html="formattedContent"></div>
        </div>
      </div>

      <div class="mt-4">
        <CommentSection />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import CommentSection from './CommentSection.vue';

const route = useRoute();
const article = ref(null);

const fetchArticle = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/articles/${route.params.id}`);
    article.value = response.data;
  } catch (error) {
    console.error('获取文章失败:', error);
  }
};

const formattedContent = computed(() => {
  if (!article.value) return '';
  return article.value.content.replace(/\n/g, '<br>');
});

const formatTime = (timeStr) => {
  return new Date(timeStr).toLocaleString('zh-CN');
};

onMounted(() => {
  fetchArticle();
});
</script>

<style scoped>
.article-container {
  max-width: 800px;
  margin: 0 auto;
}

.article-content {
  line-height: 1.8;
  font-size: 1.1rem;
}
</style> 