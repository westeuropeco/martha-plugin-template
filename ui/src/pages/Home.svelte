<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getPluginContext,
		type PluginRouteProps
	} from '@westeuropeco/martha-sdk/client';
	import Badge from '@aiaiai/design-system/components/Badge.svelte';
	import Button from '@aiaiai/design-system/components/Button.svelte';
	import EmptyState from '@aiaiai/design-system/components/EmptyState.svelte';
	import List from '@aiaiai/design-system/components/List.svelte';
	import PageContainer from '@aiaiai-pt/design-system/components/PageContainer.svelte';
	import { Plus, Trash } from 'phosphor-svelte';
	import PageHeader from '@westeuropeco/admin-chrome/PageHeader.svelte';
	import DefinitionCard from '@westeuropeco/admin-chrome/DefinitionCard.svelte';
	import { thingsApi } from '../api.js';
	import type { Thing } from '../types.js';

	// Even routes that don't read params destructure them to satisfy the
	// PluginRouteProps contract.
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	const { params: _params }: PluginRouteProps = $props();
	const ctx = getPluginContext();
	const api = thingsApi(ctx.api);

	let things = $state<Thing[]>([]);
	let loading = $state(true);
	let loadError = $state('');

	async function load() {
		loading = true;
		loadError = '';
		try {
			things = await api.list();
		} catch (e) {
			loadError = e instanceof Error ? e.message : 'Failed to load.';
			things = [];
		} finally {
			loading = false;
		}
	}

	onMount(load);

	async function handleCreate() {
		try {
			await api.create({ name: `Thing ${things.length + 1}` });
			await load();
		} catch (e) {
			ctx.toasts.error(e instanceof Error ? e.message : 'Create failed.');
		}
	}

	async function handleDelete(id: string) {
		try {
			await api.remove(id);
			await load();
		} catch (e) {
			ctx.toasts.error(e instanceof Error ? e.message : 'Delete failed.');
		}
	}
</script>

<svelte:head>
	<title>__PLUGIN_DISPLAY__ - Martha Admin</title>
</svelte:head>

<PageContainer>
	<PageHeader
		title="__PLUGIN_DISPLAY__"
		subtitle="__PLUGIN_DESCRIPTION__"
	>
		{#snippet children()}
			<Button variant="primary" onclick={handleCreate}>
				{#snippet icon()}<Plus size={16} />{/snippet}
				New thing
			</Button>
		{/snippet}
	</PageHeader>

	{#if loadError}
		<div class="load-error" role="alert">{loadError}</div>
	{/if}

	{#if loading}
		<div class="loading">Loading…</div>
	{:else if things.length === 0}
		<EmptyState
			heading="No things yet"
			body="Click 'New thing' to scaffold your first one."
		/>
	{:else}
		<List style="margin-top: var(--space-md)">
			{#each things as thing (thing.id)}
				<DefinitionCard name={thing.name} description={thing.description}>
					{#snippet badges()}
						<Badge variant="default">id: {thing.id.slice(0, 8)}</Badge>
					{/snippet}
					{#snippet actions()}
						<Button
							variant="ghost"
							size="sm"
							iconOnly
							onclick={() => ctx.navigation.goto(`/plugins/__PLUGIN_SLUG__/${thing.id}`)}
						>
							View
						</Button>
						<Button
							variant="ghost"
							size="sm"
							iconOnly
							onclick={() => handleDelete(thing.id)}
						>
							{#snippet icon()}<Trash size={14} />{/snippet}
						</Button>
					{/snippet}
				</DefinitionCard>
			{/each}
		</List>
	{/if}
</PageContainer>

<style>
	.loading {
		padding: var(--space-xl) 0;
		text-align: center;
		color: var(--color-text-secondary);
	}

	.load-error {
		padding: var(--space-md);
		margin-bottom: var(--space-md);
		border-radius: var(--radius-sm);
		background: var(--color-surface-raised);
		border: 1px solid var(--color-border);
		color: var(--color-error);
	}
</style>
