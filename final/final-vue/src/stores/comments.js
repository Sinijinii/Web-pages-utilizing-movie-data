import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useRouter } from 'vue-router';
import {useCounterStore} from '@/stores/counter'


export const useCommentsStore = defineStore('comments', () => {
    const API_URL = 'http://127.0.0.1:8000'
    const comments = ref([]);
    const sortedReviews = ref([]);
    const store = useCounterStore()
    const token = store.token
    const router = useRouter();
  
    const authHeader = computed(() => ({
      Authorization: `Token ${token.value}`,
    }));
  
    const fetchComments = async (reviewId) => {
      try {
        const res = await axios({
          url: `${API_URL}/articles/${reviewId}/comment/`,
          method: 'get',
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err.response);
      }
    };
  
    const createComment = async ({ reviewId, content }) => {
      const comment = { content };
      console.log(token);
      console.log('넘어왔니?');
      try {
        const res = await axios({
          url: `${API_URL}/articles/${reviewId}/comment/`,
          method: 'post',
          data: comment,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err.response);
      }
    };
  
    const updateComment = async ({ reviewId, commentId, content }) => {
      const comment = { content };
      try {
        const res = await axios({
          url: `${API_URL}/articles/${reviewId}/comment/${commentId}`,
          method: 'put',
          data: comment,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err.response);
      }
    };
  
    const deleteComment = async ({ reviewId, commentId }) => {
      if (confirm('정말 삭제하시겠습니까?')) {
        try {
          const res = await axios({
            url: `${API_URL}/articles/${reviewId}/comment/${commentId}`,
            method: 'delete',
            headers: {
              Authorization: `Token ${token}`
            }
          });
          comments.value = res.data;
        } catch (err) {
          console.error(err.response);
        }
      }
    };
  
    const createCommentToComment = async ({ reviewId, content, superCommentId }) => {
      const commentToComment = { content };
      try {
        const res = await axios({
  
          url: `${API_URL}/articles/${reviewId}/comment/${superCommentId}`,
          method: 'post',
          data: commentToComment,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value.push(res.data);
      } catch (err) {
        console.error(err);
      }
    };
  
    const updateCommentToComment = async ({ reviewId, content, superCommentId }) => {
      const commentToComment = { content };
      try {
        const res = await axios({
          
          url: `${API_URL}/articles/${reviewId}/comment/${superCommentId}`,
          method: 'put',
          data: commentToComment,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err);
      }
    };
  
    const deleteCommentToComment = async ({ reviewId, content, superCommentId }) => {
      const commentToComment = { content };
      try {
        const res = await axios({
          url: `${API_URL}/articles/${reviewId}/comment/${superCommentId}`,
          method: 'put',
          data: commentToComment,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err);
      }
    };
  
    const likeComment = async ({ reviewId, currentUserId, commentId }) => {
      try {
        const res = await axios({
          url: `${API_URL}/articles/${reviewId}/like/${commentId}`,
          method: 'post',
          data: currentUserId,
          headers: {
            Authorization: `Token ${token}`
          }
        });
        comments.value = res.data;
      } catch (err) {
        console.error(err);
      }
    };
  
  
    return {
      comments,
      sortedReviews,
      token,
      fetchComments,
      createComment,
      updateComment,
      deleteComment,
      createCommentToComment,
      updateCommentToComment,
      deleteCommentToComment,
      likeComment,
    };
  });
  