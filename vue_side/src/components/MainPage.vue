<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
      <div class="container">
        <a class="navbar-brand" href="#">吉利新能源</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#交流区">交流区</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#友情链接">友情链接</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.geely.com" target="_blank">吉利集团官网</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.geelyuniversity.com" target="_blank">吉利学院官网</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://creatorblog.com" target="_blank">创作者博客</a>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manage">管理页面</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-5 pt-4">
      <h1 class="text-center my-4">吉利新能源汽车展示</h1>
      <div class="carousel-container">
        <button class="carousel-button left btn btn-primary" @click="scrollLeft">‹</button>
        <div class="carousel" ref="carousel">
          <div v-for="car in cars" :key="car.id" class="car-card card" @click="goToArticle(car)" style="cursor: pointer;">
            <img :src="car.image" :alt="car.name" class="card-img-top">
            <div class="card-body">
              <h5 class="card-title">{{ car.name }}</h5>
              <p class="card-text">{{ car.description }}</p>
            </div>
          </div>
        </div>
        <button class="carousel-button right btn btn-primary" @click="scrollRight">›</button>
      </div>
      
      <div id="交流区" class="mt-5">
        <CommentSection />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import CommentSection from './CommentSection.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 储存汽车列表信息
const cars = ref([]);
const carousel = ref(null);

onMounted(() => {
  axios.get('http://localhost:5000/api/geely-cars')
      .then(response => {
        cars.value = response.data.cars; // 假设响应数据中包含汽车信息
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
});

const scrollLeft = () => {
  if (carousel.value) {
    carousel.value.scrollBy({ left: -300, behavior: 'smooth' });
  }
};

const scrollRight = () => {
  if (carousel.value) {
    carousel.value.scrollBy({ left: 300, behavior: 'smooth' });
  }
};

const goToArticle = (car) => {
  if (car.article) {
    router.push(`/article/${car.article.id}`);
  }
};
</script>

<style scoped>
/* 保留原有的特殊样式，其他使用Bootstrap类 */
.carousel-container {
  position: relative;
  width: 71.43%;
  margin: 60px auto;
}

.carousel {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none;
}

.carousel::-webkit-scrollbar {
  display: none;
}

.car-card {
  flex: 0 0 auto;
  width: 300px;
  margin: 0 8px;
}

.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1000;
  width: 50px;
  height: 56px;
  border-radius: 50%;
}

.carousel-button.left {
  left: -60px;
}

.carousel-button.right {
  right: -60px;
}
</style>