# bridal_api/middleware/bridal_middleware.py
import time
from datetime import datetime
from collections import defaultdict
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

# 1) Request logging (safe)
class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request.user, "username", "Anonymous")
        log_line = f"{datetime.now()} - User: {user} - Method: {request.method} - Path: {request.path}\n"
        with open("requests.log", "a", encoding="utf-8") as f:
            f.write(log_line)
        return None

# 2) Banned IPs
class BannedIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        from django.conf import settings
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")
        banned = getattr(settings, "BANNED_IPS", [])
        if ip in banned:
            return JsonResponse({"error": "Forbidden"}, status=403)
        return None

# 3) Simple rate limiting per IP for all /api/ endpoints
class RateLimitMiddleware(MiddlewareMixin):
    ip_times = defaultdict(list)
    MAX_REQUESTS = 60  # per TIME_WINDOW
    TIME_WINDOW = 60   # seconds

    def process_request(self, request):
        if request.path.startswith("/api/"):
            ip = self.get_client_ip(request)
            now = time.time()
            times = self.ip_times[ip]
            # keep only last TIME_WINDOW seconds
            self.ip_times[ip] = [t for t in times if now - t < self.TIME_WINDOW]
            if len(self.ip_times[ip]) >= self.MAX_REQUESTS:
                return JsonResponse({"error": "Too many requests. Try again later."}, status=429)
            self.ip_times[ip].append(now)
        return None

    def get_client_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")

# 4) Dress view counter (increments view_count on GET /api/dresses/<id>/)
class DressViewCountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != "GET":
            return None
        # expected URL: /api/dresses/<id>/
        parts = request.path.rstrip("/").split("/")
        if len(parts) >= 3 and parts[-2] == "dresses":
            try:
                pk = int(parts[-1])
            except (ValueError, TypeError):
                return None
            try:
                from bridal_api.models import Dress
                with transaction.atomic():
                    dress = Dress.objects.select_for_update().get(pk=pk)
                    dress.view_count = (dress.view_count or 0) + 1
                    dress.save(update_fields=["view_count"])
            except Exception:
                # don't crash the request if DB errors happen
                logger.exception("Dress view count update failed")
        return None

# 5) Custom header added to responses
class CustomHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["X-Benareyo-API"] = "benareyo-bridal-backend"
        return response
