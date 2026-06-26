<template>
    <UModal
        :open="open"
        :ui="{
            content: 'max-w-[420px] w-[min(92vw,420px)] bg-[var(--alexicon-surface)] text-[var(--alexicon-text)]',
            overlay: 'bg-black/60 backdrop-blur-sm'
        }"
        @update:open="$emit('update:open', $event)"
    >
        <template #content>
            <UCard
                variant="ghost"
                class="border-0"
                :ui="{ root: 'border-0', header: 'border-0', body: 'border-0', footer: 'border-0' }"
            >
                <template #header>
                    <div class="flex items-center justify-between gap-3">
                        <div>
                            <h2 class="font-bold">
                                {{ title }}
                            </h2>

                            <p v-if="description" class="mt-1 text-sm opacity-60">
                                {{ description }}
                            </p>
                        </div>

                        <UButton
                            icon="i-lucide-x"
                            variant="ghost"
                            color="neutral"
                            @click="cancel"
                        />
                    </div>
                </template>

                <slot />

                <template #footer>
                    <div class="flex justify-end gap-2">
                        <UButton
                            color="neutral"
                            variant="ghost"
                            @click="cancel"
                        >
                            {{ cancelLabel }}
                        </UButton>

                        <UButton
                            :color="confirmColor"
                            :loading="loading"
                            @click="confirm"
                        >
                            {{ confirmLabel }}
                        </UButton>
                    </div>
                </template>
            </UCard>
        </template>
    </UModal>
</template>

<script>
export default {
    name: 'ConfirmDialog',

    props: {
        open: {
            type: Boolean,
            default: false
        },
        title: {
            type: String,
            default: 'Confirm action'
        },
        description: {
            type: String,
            default: ''
        },
        confirmLabel: {
            type: String,
            default: 'Confirm'
        },
        cancelLabel: {
            type: String,
            default: 'Cancel'
        },
        confirmColor: {
            type: String,
            default: 'primary'
        },
        loading: {
            type: Boolean,
            default: false
        }
    },

    emits: ['update:open', 'confirm', 'cancel'],

    methods: {
        cancel() {
            this.$emit('update:open', false)
            this.$emit('cancel')
        },

        confirm() {
            this.$emit('confirm')
        }
    }
}
</script>