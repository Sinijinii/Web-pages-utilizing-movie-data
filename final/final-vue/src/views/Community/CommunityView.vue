<template>
  <div class="community">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'FollowingView' }">Following</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }">FindActor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }">ImageGenerator</RouterLink>
    </div>
    <div class="posts">
      <h1>Community Posts</h1>

      <div v-if="posts && posts.length">
        <div v-for="post in posts" :key="post?.id" class="post">
          <RouterLink v-if="post?.id" :to="{ name: 'PostDetail', params: { id: post?.id } }">View Details</RouterLink>
          <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" />
          <p>{{ post?.content }}</p>
          <p>{{ post?.created_at }}</p>
          <p>{{ post?.user.username }}</p>
          <div v-if="userstore.LoginUsername === post?.user.username">
            <RouterLink :to="{ name: 'EditPost', params: { id: post?.id } }">Edit</RouterLink>
            <button @click="deletePost(post?.id)">Delete</button>
          </div>
          
                    <span class="title"> 내용 :</span> <span>{{ post.content }}</span> <br>
          
                    <span class="title"> 작성시간 : </span> <span>{{ post.created_at }}</span> <br>
          
                    <span class="like">Likes :</span><span>{{ post.likes.length }}</span>          
          
                    <button class="likebtn" @click="toggleLike(post)">
                      {{ post.likes.includes(store.userId) ? 'Unlike' : 'Like' }}
                    </button>
                    
                      <!-- <p>Likes: {{ post.likes.length }}</p>
          
                    <p>{{ post.user.username }}</p> -->
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
                    <p>{{ reply.write_comment_user_name }}: {{ reply?.content }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>No comments available.</div>
            <input v-model="newCommentContents[post.id]" placeholder="Write a comment" />
            <button @click="createComment({ postId: post.id, content: newCommentContents[post.id] })">Submit</button>
          </div>

        </div>
      </div>
      <p v-else>No posts available.</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref, onBeforeMount } from 'vue'
import axios from 'axios'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'

const userstore = useCounterStore()
const posts = ref([])
const replyFormVisible = ref(null)
const newCommentContents = ref({})
const replyContents = ref({})

const store = useCommunity()

const fetchPosts = async () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/get_posts/`
  })
  .then((response) => {
    posts.value = response.data
  })
  .catch((error) => {
    console.error('Error fetching posts:', error)
  })
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
    // 댓글 작성 후 게시물 데이터 다시 불러오기
    fetchPostById(postId)
    newCommentContents.value[postId] = '' // 댓글 작성 후 입력 필드를 빈 값으로 설정
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
    // 대댓글 작성 후 게시물 데이터 다시 불러오기
    fetchPostById(postId)
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

onBeforeMount(() => {
  fetchPosts()
})
</script>

<style scoped>
.community {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f0f0f0;
}

.sidebar a {
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
  color: #000;
}

.posts {
  flex-grow: 1;
  padding: 20px;
}

.post {
  margin-bottom: 20px;
}

.post img {
  max-width: 200px;
  margin-top: 10px;
}

.post p {
  width: 80%;
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
