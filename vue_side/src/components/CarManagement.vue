<template>
  <div class="container mt-4">
    <h2 class="mb-4">车辆信息管理</h2>
    
    <!-- 添加导航标签页 -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'cars' }" 
           @click="activeTab = 'cars'" href="#">
          车辆管理
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'articles' }" 
           @click="activeTab = 'articles'" href="#">
          文章管理
        </a>
      </li>
    </ul>

    <!-- 车辆管理部分 -->
    <div v-if="activeTab === 'cars'">
      <!-- 车辆表单 -->
      <div class="card mb-4">
        <div class="card-header">
          <h3 class="mb-0">{{ isEditing ? '编辑车辆' : '添加新车辆' }}</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleCarSubmit">
            <div class="mb-3">
              <label class="form-label">车辆名称：</label>
              <input v-model="carForm.name" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">图片URL：</label>
              <input v-model="carForm.image" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">描述：</label>
              <textarea v-model="carForm.description" class="form-control" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary me-2">
              {{ isEditing ? '更新' : '添加' }}
            </button>
            <button v-if="isEditing" type="button" class="btn btn-secondary" @click="cancelCarEdit">
              取消
            </button>
          </form>
        </div>
      </div>

      <!-- 车辆列表 -->
      <div class="card">
        <div class="card-header">
          <h3 class="mb-0">车辆列表</h3>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>名称</th>
                  <th>图片</th>
                  <th>描述</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="car in cars" :key="car.id">
                  <td>{{ car.name }}</td>
                  <td>
                    <img :src="car.image" :alt="car.name" class="img-thumbnail" style="max-width: 100px">
                  </td>
                  <td>{{ car.description }}</td>
                  <td>
                    <button @click="editCar(car)" class="btn btn-warning btn-sm me-2">编辑</button>
                    <button @click="deleteCar(car.id)" class="btn btn-danger btn-sm">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- 文章管理部分 -->
    <div v-if="activeTab === 'articles'">
      <!-- 文章表单 -->
      <div class="card mb-4">
        <div class="card-header">
          <h3 class="mb-0">{{ isEditingArticle ? '编辑文章' : '添加新文章' }}</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleArticleSubmit">
            <div class="mb-3">
              <label class="form-label">文章标题：</label>
              <input v-model="articleForm.title" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">关联车型：</label>
              <select v-model="articleForm.car_id" class="form-select" required>
                <option value="">请选择车型</option>
                <option v-for="car in cars" :key="car.id" :value="car.id">
                  {{ car.name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label">文章内容：</label>
              <textarea v-model="articleForm.content" class="form-control" rows="10" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary me-2">
              {{ isEditingArticle ? '更新' : '添加' }}
            </button>
            <button v-if="isEditingArticle" type="button" class="btn btn-secondary" @click="cancelArticleEdit">
              取消
            </button>
          </form>
        </div>
      </div>

      <!-- 文章列表 -->
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
                    <button @click="viewArticle(article)" class="btn btn-info btn-sm me-2">查看</button>
                    <button @click="editArticle(article)" class="btn btn-warning btn-sm me-2">编辑</button>
                    <button @click="deleteArticle(article.id)" class="btn btn-danger btn-sm">删除</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeTab = ref('cars');
const cars = ref([]);
const articles = ref([]);
const isEditing = ref(false);
const isEditingArticle = ref(false);

// 车辆表单
const carForm = ref({
  id: null,
  name: '',
  image: '',
  description: ''
});

// 文章表单
const articleForm = ref({
  id: null,
  title: '',
  content: '',
  car_id: ''
});

// 获取所有车辆
const fetchCars = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/geely-cars');
    cars.value = response.data.cars;
  } catch (error) {
    console.error('获取车辆失败:', error);
  }
};

// 获取所有文章
const fetchArticles = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/articles');
    articles.value = response.data.articles;
  } catch (error) {
    console.error('获取文章失败:', error);
  }
};

// 车辆表单提交
const handleCarSubmit = async () => {
  try {
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/cars/${carForm.value.id}`, carForm.value);
    } else {
      await axios.post('http://localhost:5000/api/cars', carForm.value);
    }
    await fetchCars();
    resetCarForm();
  } catch (error) {
    console.error('操作失败:', error);
  }
};

// 文章表单提交
const handleArticleSubmit = async () => {
  try {
    console.log('提交的文章数据:', articleForm.value);
    
    if (isEditingArticle.value) {
      await axios.put(`http://localhost:5000/api/articles/${articleForm.value.id}`, articleForm.value);
    } else {
      const submitData = {
        ...articleForm.value,
        car_id: parseInt(articleForm.value.car_id)
      };
      const response = await axios.post('http://localhost:5000/api/articles', submitData);
      console.log('服务器响应:', response.data);
    }
    await fetchArticles();
    resetArticleForm();
  } catch (error) {
    console.error('操作失败:', error.response?.data || error);
    alert('添加文章失败: ' + (error.response?.data?.message || '请检查所有必填字段'));
  }
};

// 编辑车辆
const editCar = (car) => {
  carForm.value = { ...car };
  isEditing.value = true;
};

// 编辑文章
const editArticle = (article) => {
  articleForm.value = { ...article };
  isEditingArticle.value = true;
};

// 查看文章
const viewArticle = (article) => {
  router.push(`/article/${article.id}`);
};

// 删除车辆
const deleteCar = async (id) => {
  if (confirm('确定要删除这辆车吗？相关的文章也会被删除。')) {
    try {
      await axios.delete(`http://localhost:5000/api/cars/${id}`);
      await fetchCars();
      await fetchArticles();
    } catch (error) {
      console.error('删除失败:', error);
    }
  }
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

// 取消车辆编辑
const cancelCarEdit = () => {
  resetCarForm();
};

// 取消文章编辑
const cancelArticleEdit = () => {
  resetArticleForm();
};

// 重置车辆表单
const resetCarForm = () => {
  carForm.value = {
    id: null,
    name: '',
    image: '',
    description: ''
  };
  isEditing.value = false;
};

// 重置文章表单
const resetArticleForm = () => {
  articleForm.value = {
    id: null,
    title: '',
    content: '',
    car_id: ''
  };
  isEditingArticle.value = false;
};

// 格式化时间
const formatTime = (timeStr) => {
  return new Date(timeStr).toLocaleString('zh-CN');
};

onMounted(() => {
  fetchCars();
  fetchArticles();
});
</script>

<style scoped>
.nav-link {
  cursor: pointer;
}
</style> 