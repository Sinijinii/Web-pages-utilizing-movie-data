<template>
  <div class="community-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="posts-container">
      <h1 class="title">Community Posts</h1>
      <div v-if="posts && posts.length" class="posts">
        <div v-for="post in posts" :key="post?.id" class="post-card">
          <div class="post-header">
            <RouterLink :to="{ name: 'ProfileView', params: { username: post.user.username } }">
              <img :src="`${store.API_URL}${post.user.userinfo.user_image}`" alt="User Profile Image" class="profile-picture" />
            </RouterLink>
            <div>
              <RouterLink :to="{ name: 'ProfileView', params: { username: post.user.username } }" class="username">
                {{ post?.user.username }}
              </RouterLink>
              <p class="created-at">{{ formatDate(post?.created_at) }}</p>
            </div>
          </div>
          <RouterLink v-if="post?.id" :to="{ name: 'PostDetail', params: { id: post?.id } }">
            <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" class="post-image" />
          </RouterLink>
          <div class="post-content">
            <p>{{ post?.content }}</p>
          </div>
          <hr class="divider" />
          <div class="post-actions">
            <button v-if="post.like_list && post.like_list.includes(userstore.LoginUsername)" class="likebtn" @click="toggleLike(post)">
              🧡 {{ post.likes.length }}
            </button>
            <button v-else class="likebtn" @click="toggleLike(post)">
              🤍 {{ post.likes.length }}
            </button>
            <button class="comment-btn" @click="toggleComments(post?.id)">💬 {{ post.comments.length }}</button>
          </div>
          <div v-if="showComments === post?.id" class="comments">
            <div v-if="post?.comments && post?.comments.length">
              <div v-for="comment in post?.comments" :key="comment?.id" class="comment">
                <div class="comment-header">
                  <div class="comment-content">
                    <img :src="`${store.API_URL}${comment.write_comment_user.userinfo.user_image}`" alt="Commenter Profile Image" class="profile-picture" />
                    <p>{{ comment.write_comment_user.username }}: {{ comment?.content }}</p>
                  </div>
                  <p class="comment-time">{{ formatDate(comment?.created_at) }}</p>
                </div>
                <button @click="toggleReplyForm(comment?.id)" class="reply-btn">Reply</button>
                <div v-if="replyFormVisible === comment?.id" class="reply-form">
                  <input v-model="replyContents[comment?.id]" placeholder="Write a reply" class="form-control" />
                  <button @click="createCommentToComment({ postId: post?.id, superCommentId: comment?.id, content: replyContents[comment?.id] })" class="submit-btn">Submit</button>
                </div>
                <div v-if="comment?.commented && comment?.commented.length" class="replies">
                  <div v-for="reply in comment?.commented" :key="reply?.id" class="reply">
                    <div class="reply-header">
                      <div class="reply-content">
                        <img :src="`${store.API_URL}${reply.write_comment_user.userinfo.user_image}`" alt="Reply User Image" class="profile-picture" />
                        <p>{{ reply.write_comment_user.username }}: {{ reply?.content }}</p>
                      </div>
                      <p class="reply-time">{{ formatDate(reply?.created_at) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>No comments available.</div>
            <div class="new-comment-form">
              <input v-model="newCommentContents[post.id]" placeholder="Write a comment" class="form-control" />
              <button @click="createComment({ postId: post.id, content: newCommentContents[post.id] })" class="submit-btn">Submit</button>
            </div>
          </div>
        </div>
      </div>
      <p v-else>No posts available.</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref, onBeforeMount, watch } from 'vue'
import axios from 'axios'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const userstore = useCounterStore()
const posts = ref([])
const replyFormVisible = ref(null)
const newCommentContents = ref({})
const replyContents = ref({})
const showComments = ref(null)

const store = useCommunity()
const like_tf = ref({})

const fetchPosts = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/articles/get_posts/`)
    console.log('Fetched posts:', response.data) // 디버깅을 위한 로그
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

const deletePost = async (postId) => {
  axios({
    method: 'delete',
    url: `${store.API_URL}/articles/delete_post/${postId}/`,
    headers: {
      'Authorization': `Token ${userstore.token}`
    }
  })
  .then(() => {
    posts.value = posts.value.filter(post => post.id !== postId)
  })
  .catch((error) => {
    console.log(error)
  })
}

const toggleLike = (post) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/like_post/${post.id}/`,
    headers: {
      'Authorization': `Token ${store.token}`
    }
  })
    .then(response => {
      if (post.like_list && post.like_list.includes(userstore.LoginUsername)) {
        post.like_list = post.like_list.filter(username => username !== userstore.LoginUsername)
        post.likes.length -= 1
      } else {
        post.like_list.push(userstore.LoginUsername)
        post.likes.length += 1
      }
    })
    .catch(error => {
      console.error('좋아요 기능 실패했다', error)
    })
}

const createComment = async ({ postId, content }) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/${postId}/comments/`,
    headers: {
      'Authorization': `Token ${userstore.token}`
    },
    data: { content }
  })
  .then((response) => {
    fetchPostById(postId)
    newCommentContents.value[postId] = ''
  })
  .catch((error) => {
    console.error('Error creating comment:', error)
  })
}

const createCommentToComment = async ({ postId, superCommentId, content }) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/${postId}/comments/${superCommentId}/`,
    headers: {
      'Authorization': `Token ${userstore.token}`
    },
    data: { content }
  })
  .then((response) => {
    fetchPostById(postId)
    replyContents.value[superCommentId] = ''
    replyFormVisible.value = null // Hide the reply form after submission
  })
  .catch((error) => {
    console.error('Error creating reply:', error)
  })
}

const toggleReplyForm = (commentId) => {
  replyFormVisible.value = replyFormVisible.value === commentId ? null : commentId
  if (replyFormVisible.value !== null) {
    replyContents.value[replyFormVisible.value] = ''
  }
}

const fetchPostById = async (postId) => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/detail_post/${postId}/`
  })
  .then((response) => {
    const updatedPost = response.data[0]
    const postIndex = posts.value.findIndex(post => post.id === postId)
    if (postIndex !== -1) {
      posts.value[postIndex] = updatedPost
    }
  })
  .catch((error) => {
    console.error('Error fetching post by ID:', error)
  })
}

const toggleComments = (postId) => {
  showComments.value = showComments.value === postId ? null : postId
}

const formatDate = (dateString) => {
  const options = { year:'2-digit', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleString('ko-KR', options)
}

onBeforeMount(() => {
  fetchPosts()
})

// New post creation logic to auto-refresh the posts list
const route = useRoute()

watch(() => route.params, (newParams, oldParams) => {
  if (route.name === 'Community' && newParams !== oldParams) {
    fetchPosts()
  }
})
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.community-page {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #4C6A58; /* 짙은 녹색 배경 */
  min-height: 100vh; /* 화면 전체 높이 */
}

.sidebar-link {
  display: block;
  color: #FFF6E5; /* 크림색 텍스트 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-decoration: none;
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.sidebar-link.active {
  background-color: #FF7F47; /* 활성 링크의 배경색 */
  color: #FFF; /* 활성 링크의 텍스트 색상 */
}

.sidebar-link:hover {
  background-color: #333333; /* 어두운 회색 배경 */
}

.posts-container {
  background-color: #FFF6E5; /* 전체 페이지 배경색 */
  min-height: 100vh;
  flex-grow: 1;
  padding: 20px;
}

.title {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-align: center;
  margin-bottom: 20px;
}

.posts {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.post-card {
  background-color: #FAF7F5; /* 하얀색 배경 */
  border: 1px solid #ddd; /* 옅은 회색 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px; /* 카드 최대 너비를 800px로 설정 */
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.post-header {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 10px;
}

.profile-picture {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  color: #000;
  text-decoration: none;
}

.username:hover {
  text-decoration: underline;
}

.created-at {
  font-size: 0.8em;
  color: #888;
}

.post-image {
  width: 100%;
  height: 400px; /* 이미지 높이를 400px로 설정 */
  border-radius: 10px;
  margin: 10px 0;
  object-fit: cover; /* 이미지를 부모 요소에 맞게 자르기 */
}

.post-content {
  text-align: center;
  width: 100%;
}

.divider {
  width: 100%;
  border: 0.5px solid #ddd; /* 실선 추가 */
  margin: 20px 0;
}

.post-actions {
  display: flex;
  justify-content: flex-start; /* 좋아요와 댓글 버튼을 가까이 */
  gap: 10px; /* 버튼 사이 간격 조절 */
  width: 100%;
}

.likebtn {
  background-color: #FF7F47;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  font-family: 'TitleMedium', sans-serif;
  color: white;
}

.comment-btn {
  background-color: #4C6A58;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  font-family: 'TitleMedium', sans-serif;
  color: white;
}

.comments {
  margin-top: 20px;
  width: 100%;
}

.comment {
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 댓글 시간 오른쪽 정렬 */
}

.comment-content {
  display: flex;
  align-items: center;
}

.comment-time {
  margin-left: 10px;
  font-size: 0.8em;
  color: #888;
  white-space: nowrap;
}

.comment img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.reply-btn {
  background-color: #4C6A58;
  border: none;
  padding: 3px 7px;
  cursor: pointer;
  border-radius: 5px;
  color: white;
  font-size: 0.8em;
}

.submit-btn {
  background-color: #FF7F47;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  color: white;
  margin-top: 5px;
}

.replies {
  margin-left: 20px;
}

.reply {
  margin-bottom: 5px;
}

.reply-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 대댓글 시간 오른쪽 정렬 */
}

.reply-content {
  display: flex;
  align-items: center;
}

.reply-time {
  margin-left: 10px;
  font-size: 0.8em;
  color: #888;
  white-space: nowrap;
}

.reply img {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  margin-right: 10px;
}

.reply-form,
.new-comment-form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 10px;
}
</style>
