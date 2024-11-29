<template>
  <div class="container mt-4">
    <h2 class="mb-4">文章管理</h2>

    <div class="card mb-4">
      <div class="card-header">
        <h3 class="mb-0">{{ isEditing ? '编辑文章' : '添加新文章' }}</h3>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label class="form-label">文章标题：</label>
            <input v-model="articleForm.title" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">关联车型：</label>
            <select v-model="articleForm.car_id" class="form-select" required>
              <option v-for="car in cars" :key="car.id" :value="car.id">
                {{ car.name }}
              </option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">文章内容：</label>
            <textarea 
              v-model="articleForm.content" 
              class="form-control" 
              rows="10"
              required
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary me-2">
            {{ isEditing ? '更新' : '添加' }}
          </button>
          <button 
            v-if="isEditing" 
            type="button" 
            class="btn btn-secondary"
            @click="cancelEdit"
          >
            取消
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="mb-0">文章列表</h3>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>标题</th>
                <th>关联车型</th>
                <th>发布时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="article in articles" :key="article.id">
                <td>{{ article.title }}</td>
                <td>{{ article.car_name }}</td>
                <td>{{ formatTime(article.created_at) }}</td>
                <td>
                  <button 
                    @click="editArticle(article)" 
                    class="btn btn-warning btn-sm me-2"
                  >
                    编辑
                  </button>
                  <button 
                    @click="deleteArticle(article.id)" 
                    class="btn btn-danger btn-sm"
                  >
                    删除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const articles = ref([]);
const cars = ref([]);
const isEditing = ref(false);
const articleForm = ref({
  id: null,
  title: '',
  content: '',
  car_id: ''
});

// 获取所有文章
const fetchArticles = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/articles');
    articles.value = response.data.articles;
  } catch (error) {
    console.error('获取文章失败:', error);
  }
};

// 获取所有车型
const fetchCars = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/geely-cars');
    cars.value = response.data.cars;
  } catch (error) {
    console.error('获取车型失败:', error);
  }
};

// 提交表单
const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/articles/${articleForm.value.id}`, articleForm.value);
    } else {
      await axios.post('http://localhost:5000/api/articles', articleForm.value);
    }
    await fetchArticles();
    resetForm();
  } catch (error) {
    console.error('操作失败:', error);
  }
};

// 编辑文章
const editArticle = (article) => {
  articleForm.value = { ...article };
  isEditing.value = true;
};

// 删除文章
const deleteArticle = async (id) => {
  if (confirm('确定要删除这篇文章吗？')) {
    try {
      await axios.delete(`http://localhost:5000/api/articles/${id}`);
      await fetchArticles();
    } catch (error) {
      console.error('删除失败:', error);
    }
  }
};

// 取消编辑
const cancelEdit = () => {
  resetForm();
};

// 重置表单
const resetForm = () => {
  articleForm.value = {
    id: null,
    title: '',
    content: '',
    car_id: ''
  };
  isEditing.value = false;
};

const formatTime = (timeStr) => {
  return new Date(timeStr).toLocaleString('zh-CN');
};

onMounted(() => {
  fetchArticles();
  fetchCars();
});
</script> 