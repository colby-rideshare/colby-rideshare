import os

def posthog_context(request):
    return {
        'POSTHOG_API_KEY': os.environ.get('POSTHOG_API_KEY'),
        'POSTHOG_INSTANCE_ADDRESS': os.environ.get('POSTHOG_INSTANCE_ADDRESS'),
    }