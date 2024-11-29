<template>
  <div class="comment-section">
    <h2 class="mb-4">评论区</h2>
    
    <div class="btn-group mb-4">
      <button class="btn" 
              :class="sortBy === 'time' ? 'btn-primary' : 'btn-outline-primary'"
              @click="sortBy = 'time'">
        按时间排序
      </button>
      <button class="btn"
              :class="sortBy === 'likes' ? 'btn-primary' : 'btn-outline-primary'"
              @click="sortBy = 'likes'">
        按点赞排序
      </button>
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <input v-model="authorName" 
               class="form-control mb-3" 
               placeholder="请输入您的昵称" 
               required>
        <textarea v-model="commentContent" 
                  class="form-control mb-3" 
                  placeholder="写下您的评论..." 
                  required></textarea>
        <button @click="submitComment" class="btn btn-primary">
          发表评论
        </button>
      </div>
    </div>

    <div class="comments-list">
      <div v-for="comment in comments" 
           :key="comment.id" 
           class="card mb-3">
        <div class="card-body">
          <div class="d-flex justify-content-between mb-2">
            <h5 class="card-title mb-0">{{ comment.author }}</h5>
            <small class="text-muted">{{ formatTime(comment.created_at) }}</small>
          </div>
          <p class="card-text">{{ comment.content }}</p>
          <div class="d-flex gap-2">
            <button @click="likeComment(comment)" 
                    class="btn btn-outline-primary btn-sm">
              👍 {{ comment.likes }}
            </button>
            <button @click="showReplyForm(comment)" 
                    class="btn btn-outline-secondary btn-sm">
              回复
            </button>
          </div>

          <div v-if="activeReplyId === comment.id" 
               class="card mt-3">
            <div class="card-body">
              <input v-model="replyAuthor" 
                     class="form-control mb-2" 
                     placeholder="请输入您的昵称" 
                     required>
              <textarea v-model="replyContent" 
                        class="form-control mb-2" 
                        placeholder="写下您的回复..." 
                        required></textarea>
              <div class="d-flex gap-2">
                <button @click="submitReply(comment)" 
                        class="btn btn-primary btn-sm">
                  提交回复
                </button>
                <button @click="cancelReply" 
                        class="btn btn-secondary btn-sm">
                  取消
                </button>
              </div>
            </div>
          </div>

          <div v-if="comment.replies?.length" 
               class="ms-4 mt-3 border-start ps-3">
            <div v-for="reply in comment.replies" 
                 :key="reply.id" 
                 class="mb-3">
              <div class="d-flex justify-content-between mb-1">
                <strong>{{ reply.author }}</strong>
                <small class="text-muted">{{ formatTime(reply.created_at) }}</small>
              </div>
              <p class="mb-2">{{ reply.content }}</p>
              <button @click="likeComment(reply)" 
                      class="btn btn-outline-primary btn-sm">
                👍 {{ reply.likes }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

const comments = ref([]);
const sortBy = ref('time');
const authorName = ref('');
const commentContent = ref('');
const replyAuthor = ref('');
const replyContent = ref('');
const activeReplyId = ref(null);

// 获取评论
const fetchComments = async () => {
  try {
    const response = await axios.get(`http://localhost:5000/api/comments?sort=${sortBy.value}`);
    comments.value = response.data.comments;
  } catch (error) {
    console.error('获取评论失败:', error);
  }
};

// 发表评论
const submitComment = async () => {
  if (!authorName.value || !commentContent.value) {
    alert('请填写昵称和评论内容');
    return;
  }
  
  try {
    await axios.post('http://localhost:5000/api/comments', {
      author: authorName.value,
      content: commentContent.value
    });
    commentContent.value = '';
    await fetchComments();
  } catch (error) {
    console.error('发表评论失败:', error);
  }
};

// 点赞
const likeComment = async (comment) => {
  try {
    const response = await axios.post(`http://localhost:5000/api/comments/${comment.id}/like`);
    comment.likes = response.data.likes;
  } catch (error) {
    console.error('点赞失败:', error);
  }
};

// 显示回复表单
const showReplyForm = (comment) => {
  activeReplyId.value = comment.id;
};

// 取消回复
const cancelReply = () => {
  activeReplyId.value = null;
  replyAuthor.value = '';
  replyContent.value = '';
};

// 提交回复
const submitReply = async (parentComment) => {
  if (!replyAuthor.value || !replyContent.value) {
    alert('请填写昵称和回复内容');
    return;
  }

  try {
    await axios.post('http://localhost:5000/api/comments', {
      author: replyAuthor.value,
      content: replyContent.value,
      parent_id: parentComment.id
    });
    cancelReply();
    await fetchComments();
  } catch (error) {
    console.error('回复失败:', error);
  }
};

// 格式化时间
const formatTime = (timeStr) => {
  const date = new Date(timeStr);
  return date.toLocaleString('zh-CN');
};

// 监听排序方式变化
watch(sortBy, () => {
  fetchComments();
});

onMounted(() => {
  fetchComments();
});
</script>

<style scoped>
.comment-section {
  max-width: 800px;
  margin: 0 auto;
}
</style> 