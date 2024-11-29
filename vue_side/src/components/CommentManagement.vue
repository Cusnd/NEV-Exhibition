<template>
  <div class="comment-management">
    <h2>评论管理</h2>
    
    <!-- 筛选和排序选项 -->
    <div class="filter-section">
      <div class="sort-options">
        <button :class="{ active: sortBy === 'time' }" @click="changeSortBy('time')">
          按时间排序
        </button>
        <button :class="{ active: sortBy === 'likes' }" @click="changeSortBy('likes')">
          按点赞排序
        </button>
      </div>
      <div class="search-box">
        <input 
          v-model="searchKeyword" 
          placeholder="搜索评论内容或作者..."
          @input="handleSearch"
        >
      </div>
    </div>

    <!-- 评论列表 -->
    <div class="comments-table">
      <table>
        <thead>
          <tr>
            <th>作者</th>
            <th>内容</th>
            <th>发布时间</th>
            <th>点赞数</th>
            <th>类型</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in filteredComments" :key="comment.id">
            <td>{{ comment.author }}</td>
            <td class="content-cell">{{ comment.content }}</td>
            <td>{{ formatTime(comment.created_at) }}</td>
            <td>{{ comment.likes }}</td>
            <td>{{ comment.parent_id ? '回复' : '评论' }}</td>
            <td class="action-cell">
              <button 
                class="delete-btn" 
                @click="confirmDelete(comment)"
                title="删除评论"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页控件 -->
    <div class="pagination">
      <button 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      <span>第 {{ currentPage }} 页</span>
      <button 
        :disabled="!hasMorePages"
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>

    <!-- 确认删除对话框 -->
    <div v-if="showDeleteConfirm" class="modal">
      <div class="modal-content">
        <h3>确认删除</h3>
        <p>确定要删除这条{{ selectedComment?.parent_id ? '回复' : '评论' }}吗？</p>
        <p>作者：{{ selectedComment?.author }}</p>
        <p>内容：{{ selectedComment?.content }}</p>
        <div class="modal-actions">
          <button @click="deleteComment">确认</button>
          <button @click="showDeleteConfirm = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// 状态变量
const comments = ref([]);
const sortBy = ref('time');
const searchKeyword = ref('');
const currentPage = ref(1);
const pageSize = 10;
const showDeleteConfirm = ref(false);
const selectedComment = ref(null);

// 获取评论数据
const fetchComments = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/comments?sort=${sortBy.value}`);
    comments.value = response.data.comments;
  } catch (error) {
    console.error('获取评论失败:', error);
  }
};

// 过滤和分页的计算属性
const filteredComments = computed(() => {
  let filtered = comments.value;
  
  // 搜索过滤
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    filtered = filtered.filter(comment => 
      comment.content.toLowerCase().includes(keyword) ||
      comment.author.toLowerCase().includes(keyword)
    );
  }
  
  // 分页
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return filtered.slice(start, end);
});

// 是否有更多页
const hasMorePages = computed(() => {
  return currentPage.value * pageSize < comments.value.length;
});

// 更改排序方式
const changeSortBy = (sort) => {
  sortBy.value = sort;
  currentPage.value = 1;
  fetchComments();
};

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1;
};

// 更改页码
const changePage = (page) => {
  currentPage.value = page;
};

// 确认删除对话框
const confirmDelete = (comment) => {
  selectedComment.value = comment;
  showDeleteConfirm.value = true;
};

// 删除评论
const deleteComment = async () => {
  try {
    await axios.delete(`http://localhost:5000/api/comments/${selectedComment.value.id}`);
    await fetchComments();
    showDeleteConfirm.value = false;
    selectedComment.value = null;
  } catch (error) {
    console.error('删除评论失败:', error);
  }
};

// 格式化时间
const formatTime = (timeStr) => {
  const date = new Date(timeStr);
  return date.toLocaleString('zh-CN');
};

// 组件挂载时获取数据
onMounted(() => {
  fetchComments();
});
</script>

<style scoped>
.comment-management {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.sort-options button {
  margin-right: 10px;
  padding: 8px 16px;
}

.sort-options button.active {
  background-color: #007bff;
  color: white;
}

.search-box input {
  padding: 8px;
  width: 250px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.comments-table {
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

.content-cell {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-cell {
  width: 100px;
}

.delete-btn {
  padding: 4px 8px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-btn:hover {
  background-color: #c82333;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 20px;
  align-items: center;
}

.pagination button {
  padding: 8px 16px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.modal-actions button {
  padding: 8px 16px;
}

.modal-actions button:first-child {
  background-color: #dc3545;
  color: white;
}
</style> 