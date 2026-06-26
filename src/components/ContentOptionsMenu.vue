<template>
    <UDropdownMenu :items="items">
        <UButton
            icon="i-lucide-ellipsis"
            variant="ghost"
            color="neutral"
        />
    </UDropdownMenu>

    <ConfirmDialog
        v-model:open="deleteConfirmOpen"
        :title="`Delete this ${entityType}?`"
        description="This action cannot be undone."
        confirm-label="Delete"
        confirm-color="error"
        :loading="deleting"
        @confirm="confirmDeleteEntity"
    />
</template>

<script>
import { deletePost } from '@/services/yipnet/posts'
import { deleteComment } from '@/services/yipnet/comments'
import { reportContent } from '@/services/alexicon/content'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

export default {
    name: 'ContentOptionsMenu',
    components: {
        ConfirmDialog
    },
    props: {
        entityId: {
            type: [Number, String],
            required: true
        },
        entityType: {
            type: String,
            required: true
        },
        ownerId: {
            type: [Number, String],
            required: true
        }
    },
    emits: ['deleted', 'reported', 'stats'],
    data() {
        return {
            currentUserId: localStorage.getItem('alexicon_user_id'),
            deleteConfirmOpen: false,
            deleting: false,
        }
    },
    computed: {
        isOwner() {
            return Number(this.ownerId) === Number(this.currentUserId)
        },

        items() {
            if (this.isOwner) {
                const ownerItems = []

                if (this.entityType === 'post') {
                    ownerItems.push({
                        label: 'View statistics',
                        icon: 'i-lucide-chart-no-axes-column',
                        onSelect: this.viewStats
                    })
                }

                if (this.entityType !== 'message') {
                    ownerItems.push({
                        label: 'Delete',
                        icon: 'i-lucide-trash-2',
                        color: 'error',
                        onSelect: this.deleteEntity
                    })
                }

                if (!ownerItems.length) {
                    return []
                }

                return [ownerItems]
            }

            return [
                [
                    {
                        label: 'Report',
                        icon: 'i-lucide-flag',
                        color: 'error',
                        onSelect: this.reportEntity
                    }
                ]
            ]
        },
    },

    methods: {
        viewStats() {
            this.$router.push({
                name: 'stats',
                params: {
                    type: this.entityType,
                    id: this.entityId
                }
            });
            this.$emit('stats', {
                id: this.entityId,
                type: this.entityType
            });
        },

        deleteEntity() {
            this.deleteConfirmOpen = true
        },

        async confirmDeleteEntity() {
            this.deleting = true

            try {
                if (this.entityType === 'post') {
                    await deletePost(this.entityId)
                }

                if (this.entityType === 'comment') {
                    await deleteComment(this.entityId)
                }

                this.deleteConfirmOpen = false

                this.$emit('deleted', {
                    id: this.entityId,
                    type: this.entityType
                })
            } finally {
                this.deleting = false
            }
        },

        async reportEntity() {
            const message = prompt(`Why are you reporting this ${this.entityType}?`)
            if (!message || message.trim().length < 3) return

            await reportContent(this.entityId, {
                service: 'yipnet',
                type: this.entityType,
                route: this.$route.fullPath,
                message
            })

            this.$emit('reported', {
                id: this.entityId,
                type: this.entityType
            })
        }
    }
}
</script>