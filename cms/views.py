import json
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Service, Project, Testimonial, FAQ, BlogPost, ContactSetting, HeroSetting, AboutSetting, Enquiry
from .auth import generate_token, staff_member_required

# --- Public Client Views (Read-Only) ---

def get_services(request):
    services = Service.objects.all()
    data = []
    for s in services:
        data.append({
            'id': s.id,
            'icon': s.icon,
            'title': s.title,
            'shortDesc': s.shortDesc,
            'fullDesc': s.fullDesc,
            'features': s.features,
            'specs': s.specs
        })
    return JsonResponse(data, safe=False)

def get_projects(request):
    projects = Project.objects.all()
    data = []
    for p in projects:
        image_val = p.image
        if p.image_data:
            import base64
            mime_type = p.image_mime_type or "image/png"
            try:
                data_bytes = bytes(p.image_data)
                base64_data = base64.b64encode(data_bytes).decode('utf-8')
                image_val = f"data:{mime_type};base64,{base64_data}"
            except Exception as e:
                print(f"Error encoding image to base64: {e}")
        
        data.append({
            'id': p.id,
            'title': p.title,
            'category': p.category,
            'desc': p.desc,
            'metric': p.metric,
            'metricLabel': p.metricLabel,
            'icon': p.icon,
            'tech': p.tech,
            'image': image_val,
            'file': p.file,
            'longDesc': p.longDesc or '',
            'benefits': p.benefits or [],
            'results': p.results or [],
            'price': p.price or '',
            'price_detail_html': p.price_detail_html or '',
            'standard_price': p.standard_price or '',
            'standard_original_price': p.standard_original_price or '',
            'premium_price': p.premium_price or '',
            'premium_original_price': p.premium_original_price or '',
            'standard_features': p.standard_features or [],
            'premium_features': p.premium_features or [],
            'enterprise_features': p.enterprise_features or []
        })
    return JsonResponse(data, safe=False)

def get_project(request, id):
    try:
        p = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    
    image_val = p.image
    if p.image_data:
        import base64
        mime_type = p.image_mime_type or "image/png"
        try:
            data_bytes = bytes(p.image_data)
            base64_data = base64.b64encode(data_bytes).decode('utf-8')
            image_val = f"data:{mime_type};base64,{base64_data}"
        except Exception as e:
            print(f"Error encoding image to base64: {e}")
            
    data = {
        'id': p.id,
        'title': p.title,
        'category': p.category,
        'desc': p.desc,
        'metric': p.metric,
        'metricLabel': p.metricLabel,
        'icon': p.icon,
        'tech': p.tech,
        'image': image_val,
        'file': p.file,
        'longDesc': p.longDesc or '',
        'benefits': p.benefits or [],
        'results': p.results or [],
        'price': p.price or '',
        'price_detail_html': p.price_detail_html or '',
        'standard_price': p.standard_price or '',
        'standard_original_price': p.standard_original_price or '',
        'premium_price': p.premium_price or '',
        'premium_original_price': p.premium_original_price or '',
        'standard_features': p.standard_features or [],
        'premium_features': p.premium_features or [],
        'enterprise_features': p.enterprise_features or []
    }
    return JsonResponse(data)

def get_testimonials(request):
    testimonials = Testimonial.objects.all()
    data = []
    for t in testimonials:
        data.append({
            'id': t.id,
            'name': t.name,
            'role': t.role,
            'company': t.company,
            'content': t.content,
            'rating': t.rating,
            'avatar': t.avatar
        })
    return JsonResponse(data, safe=False)

def get_faqs(request):
    faqs = FAQ.objects.all()
    data = []
    for f in faqs:
        data.append({
            'id': f.id,
            'question': f.question,
            'answer': f.answer
        })
    return JsonResponse(data, safe=False)

def get_blog_posts(request):
    search_query = request.GET.get('search', '')
    posts = BlogPost.objects.all()
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(category__icontains=search_query) | 
            Q(summary__icontains=search_query)
        )
    data = []
    for p in posts:
        data.append({
            'id': p.id,
            'title': p.title,
            'category': p.category,
            'date': p.date.strftime('%B %d, %Y') if p.date else '',
            'readTime': p.readTime,
            'summary': p.summary,
            'imageUrl': p.imageUrl
        })
    return JsonResponse(data, safe=False)

def get_contact_info(request):
    c = ContactSetting.load()
    data = {
        'email': c.email,
        'phone': c.phone,
        'address': c.address,
        'est_response': c.est_response
    }
    return JsonResponse(data)


# --- Admin Authentication & CRUD Operations ---

@csrf_exempt
def admin_login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff:
            token = generate_token(user)
            response = JsonResponse({'token': token, 'username': user.username})
            # Set secure HTTP-only cookie for the admin session
            response.set_cookie(
                'admin_token',
                token,
                max_age=86400,  # 24 hours
                httponly=True,
                samesite='Lax',
                secure=request.is_secure()
            )
            return response
        return JsonResponse({'error': 'Invalid credentials or not a staff member'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Services CRUD
@csrf_exempt
@staff_member_required
def create_service(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        service = Service.objects.create(
            id=data['id'],
            icon=data['icon'],
            title=data['title'],
            shortDesc=data['shortDesc'],
            fullDesc=data['fullDesc'],
            features=data['features'],
            specs=data['specs']
        )
        return JsonResponse({'success': True, 'id': service.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@staff_member_required
def update_delete_service(request, id):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            service.icon = data.get('icon', service.icon)
            service.title = data.get('title', service.title)
            service.shortDesc = data.get('shortDesc', service.shortDesc)
            service.fullDesc = data.get('fullDesc', service.fullDesc)
            service.features = data.get('features', service.features)
            service.specs = data.get('specs', service.specs)
            service.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        service.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Projects CRUD
@csrf_exempt
@staff_member_required
def create_project(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        image_val = data.get('image', '')
        img_data = None
        mime_type = None
        
        if image_val and image_val.startswith('data:image/'):
            import base64
            try:
                header, base64_str = image_val.split(';base64,')
                if len(base64_str) * 3 / 4 > 1024 * 1024:
                    return JsonResponse({'error': 'Image size exceeds maximum limit of 1MB'}, status=400)
                mime_type = header.replace('data:', '')
                img_data = base64.b64decode(base64_str)
                image_val = ""
            except Exception as e:
                pass

        project = Project.objects.create(
            title=data['title'],
            category=data['category'],
            desc=data['desc'],
            metric=data['metric'],
            metricLabel=data['metricLabel'],
            icon=data['icon'],
            tech=data['tech'],
            image=image_val,
            image_data=img_data,
            image_mime_type=mime_type,
            file=data.get('file'),
            longDesc=data.get('longDesc', ''),
            benefits=data.get('benefits', []),
            results=data.get('results', []),
            price=data.get('price', ''),
            price_detail_html=data.get('price_detail_html', ''),
            standard_price=data.get('standard_price', ''),
            standard_original_price=data.get('standard_original_price', ''),
            premium_price=data.get('premium_price', ''),
            premium_original_price=data.get('premium_original_price', ''),
            standard_features=data.get('standard_features', []),
            premium_features=data.get('premium_features', []),
            enterprise_features=data.get('enterprise_features', [])
        )
        return JsonResponse({'success': True, 'id': project.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@staff_member_required
def update_delete_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            image_val = data.get('image', project.image)
            
            if image_val and image_val.startswith('data:image/'):
                import base64
                try:
                    header, base64_str = image_val.split(';base64,')
                    if len(base64_str) * 3 / 4 > 1024 * 1024:
                        return JsonResponse({'error': 'Image size exceeds maximum limit of 1MB'}, status=400)
                    mime_type = header.replace('data:', '')
                    project.image_data = base64.b64decode(base64_str)
                    project.image_mime_type = mime_type
                    project.image = ""
                except Exception as e:
                    pass
            elif image_val and not image_val.startswith('data:image/'):
                project.image = image_val
                project.image_data = None
                project.image_mime_type = None
            
            project.title = data.get('title', project.title)
            project.category = data.get('category', project.category)
            project.desc = data.get('desc', project.desc)
            project.metric = data.get('metric', project.metric)
            project.metricLabel = data.get('metricLabel', project.metricLabel)
            project.icon = data.get('icon', project.icon)
            project.tech = data.get('tech', project.tech)
            project.file = data.get('file', project.file)
            project.longDesc = data.get('longDesc', project.longDesc)
            project.benefits = data.get('benefits', project.benefits)
            project.results = data.get('results', project.results)
            project.price = data.get('price', project.price)
            project.price_detail_html = data.get('price_detail_html', project.price_detail_html)
            project.standard_price = data.get('standard_price', project.standard_price)
            project.standard_original_price = data.get('standard_original_price', project.standard_original_price)
            project.premium_price = data.get('premium_price', project.premium_price)
            project.premium_original_price = data.get('premium_original_price', project.premium_original_price)
            project.standard_features = data.get('standard_features', project.standard_features)
            project.premium_features = data.get('premium_features', project.premium_features)
            project.enterprise_features = data.get('enterprise_features', project.enterprise_features)
            project.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        project.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Testimonials CRUD
@csrf_exempt
@staff_member_required
def create_testimonial(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        testimonial = Testimonial.objects.create(
            name=data['name'],
            role=data['role'],
            company=data['company'],
            content=data['content'],
            rating=data['rating'],
            avatar=data['avatar']
        )
        return JsonResponse({'success': True, 'id': testimonial.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@staff_member_required
def update_delete_testimonial(request, id):
    try:
        testimonial = Testimonial.objects.get(id=id)
    except Testimonial.DoesNotExist:
        return JsonResponse({'error': 'Testimonial not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            testimonial.name = data.get('name', testimonial.name)
            testimonial.role = data.get('role', testimonial.role)
            testimonial.company = data.get('company', testimonial.company)
            testimonial.content = data.get('content', testimonial.content)
            testimonial.rating = data.get('rating', testimonial.rating)
            testimonial.avatar = data.get('avatar', testimonial.avatar)
            testimonial.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        testimonial.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# FAQ CRUD
@csrf_exempt
@staff_member_required
def create_faq(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        faq = FAQ.objects.create(
            question=data['question'],
            answer=data['answer']
        )
        return JsonResponse({'success': True, 'id': faq.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@staff_member_required
def update_delete_faq(request, id):
    try:
        faq = FAQ.objects.get(id=id)
    except FAQ.DoesNotExist:
        return JsonResponse({'error': 'FAQ not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            faq.question = data.get('question', faq.question)
            faq.answer = data.get('answer', faq.answer)
            faq.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        faq.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# BlogPost CRUD
@csrf_exempt
@staff_member_required
def create_blog_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        date_val = data['date']
        # Convert date string (e.g. 'June 18, 2026') to Python Date object if needed
        if isinstance(date_val, str):
            try:
                date_obj = datetime.datetime.strptime(date_val, '%B %d, %Y').date()
            except ValueError:
                date_obj = datetime.date.fromisoformat(date_val)
        else:
            date_obj = date_val

        post = BlogPost.objects.create(
            title=data['title'],
            category=data['category'],
            date=date_obj,
            readTime=data['readTime'],
            summary=data['summary'],
            imageUrl=data['imageUrl']
        )
        return JsonResponse({'success': True, 'id': post.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@staff_member_required
def update_delete_blog_post(request, id):
    try:
        post = BlogPost.objects.get(id=id)
    except BlogPost.DoesNotExist:
        return JsonResponse({'error': 'Blog post not found'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            if 'date' in data:
                date_val = data['date']
                if isinstance(date_val, str):
                    try:
                        post.date = datetime.datetime.strptime(date_val, '%B %d, %Y').date()
                    except ValueError:
                        post.date = datetime.date.fromisoformat(date_val)
            
            post.title = data.get('title', post.title)
            post.category = data.get('category', post.category)
            post.readTime = data.get('readTime', post.readTime)
            post.summary = data.get('summary', post.summary)
            post.imageUrl = data.get('imageUrl', post.imageUrl)
            post.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse({'success': True})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Contact Coordinates Update
@csrf_exempt
@staff_member_required
def update_contact_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        c = ContactSetting.load()
        c.email = data.get('email', c.email)
        c.phone = data.get('phone', c.phone)
        c.address = data.get('address', c.address)
        c.est_response = data.get('est_response', c.est_response)
        c.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Hero Settings API Views
def get_hero_info(request):
    h = HeroSetting.load()
    data = {
        'badge': h.badge,
        'title_prefix': h.title_prefix,
        'title_highlight': h.title_highlight,
        'title_suffix': h.title_suffix,
        'subtitle': h.subtitle,
        'cta1_text': h.cta1_text,
        'cta1_link': h.cta1_link,
        'cta2_text': h.cta2_text,
        'cta2_link': h.cta2_link,
        'trust_indicators': h.trust_indicators
    }
    return JsonResponse(data)

@csrf_exempt
@staff_member_required
def update_hero_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        h = HeroSetting.load()
        h.badge = data.get('badge', h.badge)
        h.title_prefix = data.get('title_prefix', h.title_prefix)
        h.title_highlight = data.get('title_highlight', h.title_highlight)
        h.title_suffix = data.get('title_suffix', h.title_suffix)
        h.subtitle = data.get('subtitle', h.subtitle)
        h.cta1_text = data.get('cta1_text', h.cta1_text)
        h.cta1_link = data.get('cta1_link', h.cta1_link)
        h.cta2_text = data.get('cta2_text', h.cta2_text)
        h.cta2_link = data.get('cta2_link', h.cta2_link)
        h.trust_indicators = data.get('trust_indicators', h.trust_indicators)
        h.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def create_enquiry(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        from django.core.cache import cache
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ip:
            ip = ip.split(',')[0].strip()
        
        cache_key = f"enquiry_limit_{ip}"
        submit_count = cache.get(cache_key, 0)
        
        if submit_count >= 5:
            return JsonResponse({'error': 'Too many submissions. Please wait an hour before trying again.'}, status=429)
            
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        company = data.get('company', '').strip()
        message = data.get('message', '').strip()

        if not name or not email or not message:
            return JsonResponse({'error': 'Name, email, and message are required'}, status=400)

        enquiry = Enquiry.objects.create(
            name=name,
            email=email,
            company=company,
            message=message
        )
        
        cache.set(cache_key, submit_count + 1, 3600)
        return JsonResponse({'success': True, 'id': enquiry.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@staff_member_required
def get_enquiries(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        enquiries = Enquiry.objects.all().order_by('-created_at')
        data = []
        for eq in enquiries:
            data.append({
                'id': eq.id,
                'name': eq.name,
                'email': eq.email,
                'company': eq.company or '',
                'message': eq.message,
                'created_at': eq.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'replied': eq.replied,
                'reply_message': eq.reply_message or '',
                'replied_at': eq.replied_at.strftime('%Y-%m-%d %H:%M:%S') if eq.replied_at else None
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@staff_member_required
def delete_enquiry(request, id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        try:
            enquiry = Enquiry.objects.get(id=id)
        except Enquiry.DoesNotExist:
            return JsonResponse({'error': 'Enquiry not found'}, status=404)
        enquiry.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@staff_member_required
def reply_enquiry(request, id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        try:
            enquiry = Enquiry.objects.get(id=id)
        except Enquiry.DoesNotExist:
            return JsonResponse({'error': 'Enquiry not found'}, status=404)
        
        data = json.loads(request.body)
        reply_message = data.get('reply_message', '').strip()
        if not reply_message:
            return JsonResponse({'error': 'Reply message is required'}, status=400)
        
        import django.utils.timezone as timezone
        enquiry.reply_message = reply_message
        enquiry.replied = True
        enquiry.replied_at = timezone.now()
        enquiry.save()

        # Simulate email dispatch
        print(f"[EMAIL SIMULATION] Sending reply to {enquiry.name} <{enquiry.email}>")
        print(f"Message: {reply_message}")

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# About Settings API Views
def get_about_info(request):
    a = AboutSetting.load()
    data = {
        'title_prefix': a.title_prefix,
        'title_highlight': a.title_highlight,
        'subtitle': a.subtitle,
        'stats': a.stats,
        'values': a.values,
        'team': a.team
    }
    return JsonResponse(data)

@csrf_exempt
@staff_member_required
def update_about_info(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        a = AboutSetting.load()
        a.title_prefix = data.get('title_prefix', a.title_prefix)
        a.title_highlight = data.get('title_highlight', a.title_highlight)
        a.subtitle = data.get('subtitle', a.subtitle)
        a.stats = data.get('stats', a.stats)
        a.values = data.get('values', a.values)
        a.team = data.get('team', a.team)
        a.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

