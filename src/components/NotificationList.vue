<template>
    <section class="NotificationList-MAIN">
        <div class="mb-3 flex items-center justify-between gap-3">
            <label class="flex items-center gap-2 text-sm">
                <USwitch v-model="hideSeen" @update:model-value="loadNotifications" />
                <span>Hide read</span>
            </label>

            <UButton
                size="sm"
                variant="ghost"
                color="neutral"
                :disabled="!unreadCount"
                @click="markAllRead"
            >
                Mark all as read
            </UButton>
        </div>

        <div v-if="loading" class="rounded-lg bg-black/20 p-4 text-sm opacity-60">
            Loading notifications...
        </div>

        <div v-else-if="!notifications.length" class="rounded-lg bg-black/20 p-4 text-sm opacity-60">
            No notifications.
        </div>

        <div v-else class="space-y-2">
            <RouterLink
                v-for="notification in notifications"
                :key="notification.id"
                :to="notificationRoute(notification)"
                class="notification-item"
                :class="{ 'notification-unread': !notification.seen }"
                @click="markRead(notification)"
            >
                <UAvatar
                    :src="notificationAvatar(notification)"
                    :alt="notificationTitle(notification)"
                    size="md"
                />

                <div class="min-w-0 flex-1">
                    <p class="text-sm">
                        {{ notificationTitle(notification) }}
                    </p>

                    <p class="text-xs opacity-50">
                        {{ formatDate(notification.notif_date) }}
                    </p>
                </div>

                <UBadge
                    v-if="!notification.seen"
                    color="primary"
                    variant="soft"
                    size="xs"
                >
                    New
                </UBadge>
            </RouterLink>
        </div>
    </section>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import {
    getNotifications,
    readNotification,
    readAllNotifications
} from '@/services/alexicon/notifications'

export default {
    name: 'NotificationList',

    emits: ['unread-change'],

    props: {
        compact: {
            type: Boolean,
            default: false
        },
        limit: {
            type: Number,
            default: 20
        }
    },

    data() {
        return {
            loading: false,
            hideSeen: false,
            notifications: [],
            unreadCount: 0
        }
    },

    methods: {
        normalizeContent(notification) {
            let content = notification.content || {}

            if (typeof content === 'string') {
                try {
                    content = JSON.parse(content)
                } catch {
                    content = {}
                }
            }

            return content || {}
        },

        async loadNotifications() {
            this.loading = true

            try {
                const result = await getNotifications({
                    limit: this.limit,
                    offset: 0,
                    seen: this.hideSeen ? '0' : ''
                })

                this.notifications = result.data?.notifications || []
                this.unreadCount = Number(result.data?.unread_count || 0)
                this.$emit('unread-change', this.unreadCount)
            } finally {
                this.loading = false
            }
        },

        async markRead(notification) {
            if (notification.seen) return

            await readNotification(notification.id)
            notification.seen = 1

            this.unreadCount = Math.max(this.unreadCount - 1, 0)
            this.$emit('unread-change', this.unreadCount)

            if (this.hideSeen) {
                this.notifications = this.notifications.filter(
                    item => Number(item.id) !== Number(notification.id)
                )
            }
        },

        async markAllRead() {
            await readAllNotifications()

            this.notifications = this.notifications.map(item => ({
                ...item,
                seen: 1
            }))

            if (this.hideSeen) {
                this.notifications = []
            }

            this.unreadCount = 0
            this.$emit('unread-change', 0)
        },

        notificationTitle(notification) {
            const content = this.normalizeContent(notification)

            if (notification.event === 'follow' || content.follower_id) {
                return `${content.name || 'Someone'} follows you.`
            }

            if (notification.event === 'comment' || content.commentId) {
                return `${content.user?.name || 'Someone'} commented on your post.`
            }

            if (notification.event === 'vote' || content.voteType) {
                if (content.entityType === 'message') {
                    return `${content.user?.name || 'Someone'} reacted '${content.voteType}' to your message.`
                }
                if (content.entityType === 'comment') {
                    return `${content.user?.name || 'Someone'} reacted '${content.voteType}' to your comment.`
                }
                return `${content.user?.name || 'Someone'} reacted '${content.voteType}' to your post.`
            }

            if (notification.event === 'message' || content.messageId) {
                return `Message from ${content.user?.name || 'Someone'}: "${content.preview || ''}"`
            }

            if (content.sharedPostId) {
                return `${content.user?.name || 'Someone'} shared your post.`
            }

            if (notification.event === 'mention') {
                if (content.entityType === 'comment') {
                    return `${content.user?.name || 'Someone'} mentioned you in a comment.`
                }
                return `${content.user?.name || 'Someone'} mentioned you in a post.`
            }

            return notification.event || 'Notification'
        },

        notificationRoute(notification) {
            const content = this.normalizeContent(notification)

            if (content.follower_id) {
                return `/user/${content.follower_id}`
            }

            if (content.entityType === 'comment') {
                const commentId = content.commentId || content.targetId

                if (content.postId) {
                    return `/post/${content.postId}#CommentRenderer-${commentId}`
                }

                return '/notifications'
            }

            if (content.postId && content.commentId) {
                return `/post/${content.postId}#CommentRenderer-${content.commentId}`
            }

            if (content.sharedPostId) {
                return `/post/${content.sharedPostId}`
            }

            if (content.entityType === 'message' && content.conversation_id) {
                return `/chat/${content.conversation_id}#MessageRenderer-${content.targetId}`
            }

            if (content.messageId && content.conversation_id) {
                return `/chat/${content.conversation_id}#MessageRenderer-${content.messageId}`
            }

            if (notification.event === 'mention') {
                if (content.entityType === 'comment') {
                    return `/post/${content.postId}#CommentRenderer-${content.commentId || content.targetId}`
                }

                return `/post/${content.postId || content.targetId}`
            }

            if (content.targetId) {
                return `/post/${content.targetId}`
            }

            return '/notifications'
        },

        notificationAvatar(notification) {
            const content = this.normalizeContent(notification)

            const value =
                content.user?.profile_pic ||
                content.user?.current_profile_pic ||
                content.current_profile_pic ||
                content.profile_pic ||
                ''

            if (!value) return ''

            if (String(value).startsWith('/')) {
                return `${API_URL}${value}`
            }

            return `${API_URL}/alexicon/media/${value}`
        },

        formatDate(date) {
            if (!date) return ''

            return new Date(date).toLocaleString('es-MX', {
                dateStyle: 'medium',
                timeStyle: 'short'
            })
        },

        handleRealtimeNotification() {
            this.loadNotifications()
        },
    },
    mounted() {
        this.loadNotifications()
        window.addEventListener('alexicon-notification', this.handleRealtimeNotification)
    },
    beforeUnmount() {
        window.removeEventListener('alexicon-notification', this.handleRealtimeNotification)
    }
}
</script>

<style scoped lang="stylus">
.NotificationList-MAIN
    width 100%

.notification-item
    display flex
    align-items center
    gap 0.75rem
    padding 0.75rem
    border-radius 10px
    color inherit
    text-decoration none
    background rgba(0, 0, 0, 0.18)
    border-left 4px solid rgba(128, 128, 128, 0.25)
    transition all 0.15s

    &:hover
        background #3a3a3a
        color white

.notification-unread
    border-left-color #7700ff
    background rgba(119, 0, 255, 0.12)
</style>