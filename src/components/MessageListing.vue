<template>
    <aside class="MessageListing-MAIN space-y-2">
        <div v-if="loading" class="p-3 text-sm opacity-60">
            Loading chats...
        </div>

        <div v-else-if="!conversations.length" class="p-3 text-sm opacity-60">
            No conversations yet.
        </div>

        <div class="mb-3 flex items-center justify-between">
            <h2 class="font-semibold">Chats</h2>
            <UButton
                icon="i-lucide-square-pen"
                size="sm"
                color="primary"
                variant="soft"
                @click="$emit('new-chat')"
            />
        </div>

        <RouterLink
            v-for="conversation in conversations"
            :key="conversation.id"
            :to="`/chat/${conversation.id}`"
            class="conversation-item"
            :class="{ 'conversation-item-active': Number($route.params.id) === Number(conversation.id) }"
        >
            <UAvatar
                v-if="!conversation.is_group"
                :src="avatarUrl(conversation.display_pic)"
                :alt="conversation.display_name || 'Chat'"
                size="md"
            />

            <UAvatarGroup v-else size="md" :max="4">
                <UAvatar
                    v-for="user in conversation.other_participants.slice(0, 4)"
                    :key="user.id"
                    :src="avatarUrl(user.profile_pic)"
                    :alt="`${user.name} ${user.surname}`"
                />
            </UAvatarGroup>

            <div class="min-w-0 flex-1">
                <p class="truncate text-sm font-semibold">
                    {{ conversation.display_name || conversation.name || 'Conversation' }}
                </p>

                <p class="truncate text-xs opacity-75">
                    {{ conversation.last_message || 'No messages yet.' }}
                </p>

                <p v-if="conversation.last_message_date" class="truncate shrink-0 text-[10px] opacity-50">
                    {{ shortDate(conversation.last_message_date) }}
                </p>
            </div>
        </RouterLink>
    </aside>
</template>

<script>
const API_URL = import.meta.env.VITE_API_URL

import { getConversations } from '@/services/yipnet/messages'

export default {
    name: 'MessageListing',
    emits: ['loaded', 'new-chat'],
    data() {
        return {
            loading: false,
            conversations: []
        }
    },
    methods: {
        avatarUrl(value) {
            if (!value) return ''

            if (String(value).startsWith('/')) {
                return `${API_URL}${value}`
            }

            return `${API_URL}/alexicon/media/${value}`
        },

        shortDate(date) {
            if (!date) return ''

            return new Date(date).toLocaleString('es-MX', {
                day: '2-digit',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit'
            })
        },

        async loadConversations() {
            this.loading = true

            try {
                const result = await getConversations()
                this.conversations = result.data?.conversations || []
                this.$emit('loaded', this.conversations)
            } finally {
                this.loading = false
            }
        }
    },
    mounted() {
        this.loadConversations()
    }
}
</script>

<style scoped lang="stylus">
.MessageListing-MAIN
    width 100%

.conversation-item
    display flex
    align-items center
    gap 0.75rem
    padding 0.75rem
    border-radius 10px
    color inherit
    text-decoration none
    background transparent
    transition all 0.15s

    &:hover
        background #3a3a3a
        color white

.conversation-item-active
    background #3a3a3a
    color white
</style>