<template>
  <div class="movie-detail-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'MainView' }" class="sidebar-link" :class="{ active: $route.name === 'Mainpage' }">Mainpage</RouterLink>
      <hr>
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView', params: { username: userstore.LoginUsername } }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="post-detail">
      <div class="post-header">
        <RouterLink :to="{ name: 'ProfileView', params: { username: post?.user.username } }">
          <img :src="`${store.API_URL}${post.user.userinfo.user_image}`" alt="User Profile Picture" class="profile-picture" />
        </RouterLink>
        <div>
          <RouterLink :to="{ name: 'ProfileView', params: { username: post?.user.username } }" class="username">
            {{ post?.user.username }}
          </RouterLink>
          <p class="created-at">{{ formatDate(post?.created_at) }}</p>
        </div>
      </div>
      <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" class="post-image" />
      <p class="post-content">{{ post?.content }}</p>

      <div class="post-actions">
        <div class="like-section">
          <button v-if="post.like_list && post.like_list.includes(userstore.LoginUsername)" class="likebtn" @click="toggleLike(post)">
              🧡 {{ post.likes.length }}
            </button>
            <button v-else class="likebtn" @click="toggleLike(post)">
              🤍 {{ post.likes.length }}
            </button>
        </div>
        <div v-if="userstore.LoginUsername === post?.user.username" class="edit-delete-buttons">
          <RouterLink :to="{ name: 'EditPost', params: { id: postid } }" class="btn btn-primary me-2">📝</RouterLink>
          <button @click="deletePost(postid)" class="btn btn-danger">🗑️</button>
        </div>
      </div>

      <!-- 댓글 섹션 시작 -->
      <div class="comments-section">
        <h5>댓글</h5>
        <div v-if="post?.comments && post?.comments.length">
          <div v-for="comment in post?.comments" :key="comment?.id" class="comment">
            <div class="comment-header">
              <div class="comment-user-info">
                <RouterLink :to="{ name: 'ProfileView', params: { username: comment.write_comment_user.username } }">
                  <img :src="`${store.API_URL}${comment.write_comment_user.userinfo.user_image}`" alt="Commenter Profile Image" class="profile-picture" />
                </RouterLink>
                <div>
                  <RouterLink :to="{ name: 'ProfileView', params: { username: comment.write_comment_user.username } }" class="comment-user">
                    {{ comment.write_comment_user.username }}:
                  </RouterLink>
                  <p class="comment-content">{{ comment?.content }}</p>
                </div>
              </div>
              <p class="created-at">{{ formatDate(comment?.created_at) }}</p>
            </div>
            <button @click="toggleReplyForm(comment?.id)" class="reply-btn">Reply</button>
            <div v-if="replyFormVisible === comment?.id" class="reply-form">
              <input v-model="replyContents[comment?.id]" placeholder="Write a reply" class="form-control" />
              <button @click="createCommentToComment({ postId: post?.id, superCommentId: comment?.id, content: replyContents[comment?.id] })" class="btn btn-success mt-2">Submit</button>
            </div>
            <div v-if="comment?.commented && comment?.commented.length" class="replies">
              <div v-for="reply in comment?.commented" :key="reply?.id" class="reply">
                <div class="reply-header">
                  <div class="reply-user-info">
                    <RouterLink :to="{ name: 'ProfileView', params: { username: reply.write_comment_user.username } }">
                      <img :src="`${store.API_URL}${reply.write_comment_user.userinfo.user_image}`" alt="Reply User Image" class="profile-picture" />
                    </RouterLink>
                    <div>
                      <RouterLink :to="{ name: 'ProfileView', params: { username: reply.write_comment_user.username } }" class="reply-user">
                        {{ reply.write_comment_user.username }}:
                      </RouterLink>
                      {{ reply.write_comment_user.username }}:
                      <p class="reply-content">{{ reply?.content }}</p>
                    </div>
                  </div>
                  <p class="created-at">{{ formatDate(reply?.created_at) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else>No comments available.</div>
        <div class="new-comment-form">
          <input v-model="newCommentContent" placeholder="Write a comment" class="form-control" />
          <button @click="createComment({ postId: post?.id, content: newCommentContent })" class="btn btn-primary mt-2">Submit</button>
        </div>
      </div>
      <!-- 댓글 섹션 끝 -->
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { useCommunity } from '@/stores/community'

const route = useRoute()
const store = useCommunity()
const userstore = useCounterStore()

const postid = route.params.id

const router = useRouter()

const post = ref(null)
const replyFormVisible = ref(null)
const newCommentContent = ref('')
const replyContents = ref({})

const toggleLike = (post) => {
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/like_post/${post.id}/`,
    headers: {
      'Authorization': `Token ${userstore.token}`
    }
  })
    .then(response => {
      const liked = response.data.liked
      if (liked) {
        post.likes.push(store.userId)
      } else {
        const index = post.likes.indexOf(store.userId)
        if (index > -1) {
          post.likes.splice(index, 1)
        }
      }
    })
    .catch(error => {
      console.error('좋아요 기능 실패했다', error)
    })
}

const fetchPost = async () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/detail_post/${postid}/`,
  })
  .then(response => {
    post.value = response.data[0]
  })
  .catch(error => {
    console.log(error)
  })
}

const deletePost = async (postId) => {
  try {
    await axios.delete(`${store.API_URL}/delete_post/${postId}/`, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    router.push({ name: 'Community' })
  } catch (error) {
    console.error('Error deleting post:', error)
  }
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
    fetchPost()  // 댓글 작성 후 게시물 데이터 다시 불러오기
    newCommentContent.value = '' // 댓글 작성 후 입력 필드를 빈 값으로 설정
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
    fetchPost()  // 대댓글 작성 후 게시물 데이터 다시 불러오기
    replyContents.value[superCommentId] = '' // 대댓글 작성 후 입력 필드를 빈 값으로 설정
    replyFormVisible.value = null // 대댓글 작성 후 폼 숨기기
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

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

onBeforeMount(() => {
  fetchPost()
})
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.movie-detail-page {
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

.post-detail {
  flex-grow: 1;
  padding: 20px;
  background-color: #FAF7F5; /* 크림색 배경 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-picture {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  color: #4C6A58;
  text-decoration: none;
}

.created-at {
  font-size: 0.9em;
  color: #888;
}

.post-image {
  width: 80%; /* 너비를 80%로 설정하여 중앙에 배치 */
  height: auto;
  border-radius: 10px;
  margin: 0 auto 20px; /* 상하 여백과 중앙 정렬 */
  display: block;
}

.post-content {
  margin-bottom: 20px;
  font-family: 'BatangRegular', serif;
  color: #333;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}

.like-section {
  display: flex;
  align-items: center;
  gap: 10px;
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

.edit-delete-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.comments-section {
  margin-top: 20px;
}

.comment {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.comment-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.comment-user-info {
  display: flex;
  align-items: center;
}

.comment img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
}

.comment-user {
  font-weight: bold;
  color: #4C6A58;
  text-decoration: none;
}

.comment-content {
  color: #333;
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

.reply-form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 10px;
}

.new-comment-form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 20px;
}

.replies {
  margin-left: 20px;
  margin-top: 10px;
}

.reply {
  margin-bottom: 5px;
  padding-bottom: 5px;
  border-bottom: 1px solid #ddd;
}

.reply-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reply-user-info {
  display: flex;
  align-items: center;
}

.reply img {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  margin-right: 10px;
}

.reply-user {
  font-weight: bold;
  color: #4C6A58;
  text-decoration: none;
}

.reply-content {
  color: #333;
}
</style>
