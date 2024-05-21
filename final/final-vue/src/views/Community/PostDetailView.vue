<template>
  <div class="post-detail">
    <h1>{{ postid }}번 Post</h1>
    <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" />
    <p>{{ post?.content }}</p>
    <p>{{ post?.created_at }}</p>
    <p>{{ post?.user.username }}</p>
    <div v-if="userstore.LoginUsername === post?.user.username">
      <RouterLink :to="{ name: 'EditPost', params: { id: postid } }">Edit</RouterLink>
      <button @click="deletePost(postid)">Delete</button>
    </div>
    
    <!-- 댓글 섹션 시작 -->
    <div class="comments">
      <h3>Comments</h3>
      <div v-if="post?.comments && post?.comments.length">
        <div v-for="comment in post?.comments" :key="comment?.id" class="comment">
          <p>{{ comment.write_comment_user_name }}: {{ comment?.content }}</p>
          <button @click="toggleReplyForm(comment?.id)">Reply</button>
          <div v-if="replyFormVisible === comment?.id">
            <input v-model="replyContents[comment?.id]" placeholder="Write a reply" />
            <button @click="createCommentToComment({ postId: post?.id, superCommentId: comment?.id, content: replyContents[comment?.id] })">Submit</button>
          </div>
          <div v-if="comment?.commented && comment?.commented.length" class="replies">
            <div v-for="reply in comment?.commented" :key="reply?.id" class="reply">
              <p>{{ reply?.write_comment_user_name }}: {{ reply?.content }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else>No comments available.</div>
      <input v-model="newCommentContent" placeholder="Write a comment" />
      <button @click="createComment({ postId: post?.id, content: newCommentContent })">Submit</button>
    </div>
    <!-- 댓글 섹션 끝 -->
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

onBeforeMount(() => {
  fetchPost()
})
</script>

<style scoped>
.post-detail {
  padding: 20px;
}

.post-detail img {
  max-width: 100%;
  margin-top: 10px;
}

.post-detail p {
  margin-top: 10px;
}

.post-detail button {
  margin-top: 10px;
}

.comments {
  margin-top: 20px;
}

.comment {
  margin-bottom: 10px;
}

.replies {
  margin-left: 20px;
}

.reply {
  margin-bottom: 5px;
}
</style>
