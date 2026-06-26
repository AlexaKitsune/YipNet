import { createRouter, createWebHistory } from 'vue-router'
import { getSession } from '@/services/alexicon/auth'

import Feed from '../views/Feed.vue'
import Access from '../views/Access.vue'
import Search from '../views/Search.vue'
import Post from '../views/Post.vue'
import Profile from '../views/Profile.vue'
import Chat from '../views/Chat.vue'
import Notifications from '../views/Notifications.vue'
import Settings from '../views/Settings.vue'
import NotFound from '../views/NotFound.vue'
import Stats from '../views/Stats.vue'
import AtRedirect from '../views/AtRedirect.vue'

const routes = [
    { path: '/', name: 'feed', component: Feed, meta: { requiresAuth: true } },
    { path: '/access', name: 'access', component: Access, meta: { guestOnly: true } },
    { path: '/search', name: 'search', component: Search, meta: { requiresAuth: true } },
    { path: '/post/:id', name: 'post', component: Post, meta: { requiresAuth: true } },
    { path: '/stats/:type/:id', name: 'stats', component: Stats, meta: { requiresAuth: true } },
    { path: '/user/:id', name: 'profile', component: Profile, meta: { requiresAuth: true } },
    { path: '/at/:at', name: 'at-redirect', component: AtRedirect, meta: { requiresAuth: true } },
    { path: '/chat', name: 'chat', component: Chat, meta: { requiresAuth: true } },
    { path: '/chat/:id', name: 'chat-conversation', component: Chat, meta: { requiresAuth: true } },
    { path: '/chat/user/:userId', name: 'chat-user', component: Chat, meta: { requiresAuth: true } },
    { path: '/notifications', name: 'notifications', component: Notifications, meta: { requiresAuth: true } },
    { path: '/settings', name: 'settings', component: Settings, meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(async (to) => {
    const token = localStorage.getItem('alexicon_token')
    
    if (to.meta.guestOnly && token)
        return { name: 'feed' }
    if (!to.meta.requiresAuth)
        return true
    if (!token)
        return { name: 'access' }

    try {
        await getSession()
        return true
    } catch {
        localStorage.removeItem('alexicon_token')
        localStorage.removeItem('alexicon_user_id')
        return { name: 'access' }
    }
})

export default router