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

        <div v-for="post in posts" :key="post.id" class="post">
        
          <RouterLink :to="{ name: 'PostDetail', params: { id: post?.id } }">View Details</RouterLink> |

          <button @click="deletePost(post?.id)">Delete</button> |

          <RouterLink :to="{ name: 'EditPost', params: { id: post?.id } }">Edit</RouterLink> |

          <br>
          <img :src="`${store.API_URL}${post.image}`" alt="Post Image" />

          <p>{{ post?.content }}</p>

          <p>{{ post?.created_at }}</p>

          <p>Likes: {{ post.likes.length }}</p>

          <button @click="toggleLike(post)">
            {{ post.likes.includes(store.userId) ? 'Unlike' : 'Like' }}
          </button>


        </div>
      </div>
    </div>

</template>



<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import router from '@/router';
import { useCounterStore } from '@/stores/counter'

const posts = ref([])

const store = useCounterStore()
console.log(router)

const fetchPosts = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/articles/get_posts/`)
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

const deletePost = async (postId) => {
  try {
    await axios.delete(`${store.API_URL}/articles/delete_post/${postId}/`, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    posts.value = posts.value.filter(post => post.id !== postId)
  } catch (error) {
    console.error('Error deleting post:', error)
  }
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



onMounted(fetchPosts)
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
</style>