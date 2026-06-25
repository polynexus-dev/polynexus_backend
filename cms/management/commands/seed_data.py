import datetime
from django.core.management.base import BaseCommand
from cms.models import Service, Project, Testimonial, FAQ, BlogPost, ContactSetting, HeroSetting

class Command(BaseCommand):
    help = 'Seeds dummy content data matching the frontend'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database content...')

        # 1. Seed Service Data
        services_data = [
            {
                'id': 'design',
                'icon': 'Zap',
                'title': 'Adaptive Design Systems',
                'shortDesc': 'Architecting flexible, component-based user interfaces that evolve with your business logic and brand identity.',
                'fullDesc': 'Build unified component ecosystems, flexible UI architecture, and automated design token deployment pipelines that scale across mobile, web, and enterprise surfaces seamlessly.',
                'features': [
                    'Automated component assembly pipelines',
                    'Adaptive styling token generation',
                    'Comprehensive cross-platform layout APIs'
                ],
                'specs': {
                    'Framework': 'React / Tailwind v4',
                    'Speed': '100% Core Performance',
                    'Accessibility': 'WCAG AA Compliant'
                }
            },
            {
                'id': 'governance',
                'icon': 'Database',
                'title': 'Unified Data Governance',
                'shortDesc': 'Designing centralized and secure data structures that break down silos across your operational ecosystem.',
                'fullDesc': 'Establish structural transactional log audits, active-active cloud database partitions, and enterprise-grade schema lifecycle protocols with strict compliance.',
                'features': [
                    'Active-active multi-region syncing',
                    'Real-time schema trace logs',
                    'Cryptographic compliance validation'
                ],
                'specs': {
                    'Architecture': 'Distributed Sync',
                    'Auditing': 'Continuous Event Logs',
                    'Security': 'RBAC Access Policies'
                }
            },
            {
                'id': 'security',
                'icon': 'Shield',
                'title': 'Secured Business Logic Pipelines',
                'shortDesc': 'Implementing zero-trust architecture and cryptographic validation to protect your entire process workflow.',
                'fullDesc': 'Protect data payloads, routine workflows, and custom backend modules using zero-trust function boundaries, E2EE parameters, and automated security scanning layers.',
                'features': [
                    'Zero-trust gateway authentication',
                    'AES-GCM-256 encrypted isolation',
                    'Continuous threat heuristic monitoring'
                ],
                'specs': {
                    'Protocol': 'WASM Isolation Boundary',
                    'Validation': '< 0.15ms runtime checks',
                    'Compliance': 'SOC2 / HIPAA native'
                }
            },
            {
                'id': 'allocation',
                'icon': 'Layers',
                'title': 'Intelligent Resource Allocation',
                'shortDesc': 'Dynamic and automated resource provisioning to ensure peak system performance and cost efficiency, tailored to demand.',
                'fullDesc': 'Deploy and schedule background jobs onto low-cost, low-latency computing node clusters globally using neural routing models and CPU resource benchmarks.',
                'features': [
                    'AI-predictive routine routing',
                    'Self-healing cluster topologies',
                    'Sub-atomic runtime scheduling'
                ],
                'specs': {
                    'Engine': 'Neural scheduler',
                    'Protocols': 'gRPC / HTTP3 routing',
                    'Nodes': '14k+ active global servers'
                }
            }
        ]

        for s in services_data:
            Service.objects.update_or_create(
                id=s['id'],
                defaults={
                    'icon': s['icon'],
                    'title': s['title'],
                    'shortDesc': s['shortDesc'],
                    'fullDesc': s['fullDesc'],
                    'features': s['features'],
                    'specs': s['specs']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(services_data)} services.'))

        # 2. Seed Project Data
        self.stdout.write('Clearing legacy projects...')
        Project.objects.all().delete()

        projects_data = [
            {
                'title': 'Mail Service Software',
                'category': 'polynexus',
                'desc': 'High-throughput enterprise mail server software supporting transactional relays and spam-filtering layers.',
                'metric': '99.999%',
                'metricLabel': 'Uptime Delivery',
                'icon': 'Zap',
                'tech': ['Node.js', 'Redis', 'SMTP', 'Docker'],
                'image': 'https://images.unsplash.com/photo-1557200134-90327ee9fafa?auto=format&fit=crop&q=80&w=400&h=250',
                'file': 'mail-service-relay.sh',
                'longDesc': 'Our Mail Service Software provides an enterprise-ready SMTP transaction gateway tailored for massive scale. By separating incoming relays from outgoing transactional queues, we achieved a resilient routing architecture that tolerates sudden load bursts and external API latencies. Additionally, we integrated a signature-based real-time spam filter running directly on memory caches for negligible processing delay.',
                'benefits': [
                    'Ensures transactional messages are delivered instantly, boosting user trust.',
                    'Provides real-time security shielding against spam and threat payloads.'
                ],
                'results': [
                    'Delivered 99.999% uptime SLA continuously over 12 months.',
                    'Reduced average delivery latency to under 350ms globally.'
                ]
            },
            {
                'title': 'Pench Milk Delivery System',
                'category': 'custom',
                'desc': 'Custom route optimization and subscription management system for dairy distribution operations.',
                'metric': '10k+ Liters/Day',
                'metricLabel': 'Milk Distributed',
                'icon': 'Database',
                'tech': ['React Native', 'Django', 'PostgreSQL', 'Google Maps API'],
                'image': 'https://images.unsplash.com/photo-1546483875-ad9014c88eba?auto=format&fit=crop&q=80&w=400&h=250',
                'file': 'milk-distribution-api.sh',
                'longDesc': 'The Pench Milk Delivery System digitizes the distribution chain of fresh milk from farms to households. We built an offline-first mobile app for delivery agents, backed by a robust Django engine that handles daily route calculations based on geography, driver capacity, and current traffic conditions. An integrated customer portal allows flexible subscription management and instant notifications.',
                'benefits': [
                    'Optimizes delivery routes automatically to decrease logistics overhead.',
                    'Guarantees reliable offline functionality for remote updates.'
                ],
                'results': [
                    'Optimized daily delivery miles by 24%, reducing vehicle fuel overheads.',
                    'Successfully scaling distributions past 10,000 liters of milk per day.'
                ]
            },
            {
                'title': 'Enterprise ERP Software',
                'category': 'polynexus',
                'desc': 'Modular management tool synchronizing production schedules, ledger accounting, and raw material inventory.',
                'metric': '35%',
                'metricLabel': 'Operational Savings',
                'icon': 'Cpu',
                'tech': ['PostgreSQL', 'React', 'Python', 'Django'],
                'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=400&h=250',
                'file': None,
                'longDesc': 'This bespoke Enterprise ERP solution unifies fragmented workflows within heavy manufacturing environments. By integrating raw inventory ledgers directly with machine scheduling, the plant managers gain automatic forecasting on stock levels, labor requirements, and machinery load. A double-entry accounting engine underpins every invoice and purchase order, ensuring total transparency.',
                'benefits': [
                    'Unifies all regional office records into a singular, high-speed data source.',
                    'Automates auditing procedures to prevent stock and invoice drifts.'
                ],
                'results': [
                    'Generated 35% operational savings by eliminating raw material inventory surplus.',
                    'Decreased month-end closing cycles from 12 days to just 2 hours.'
                ]
            },
            {
                'title': 'Enterprise CRM Software',
                'category': 'polynexus',
                'desc': 'Customer relationship platform tracking sales pipelines, support interactions, and agent response latency.',
                'metric': '18x',
                'metricLabel': 'Sales Conversion',
                'icon': 'Globe',
                'tech': ['React', 'TypeScript', 'WebSockets', 'Django REST'],
                'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=400&h=250',
                'file': None,
                'longDesc': 'A fast, real-time CRM platform targeting quick-response support desks and modern sales operations. Incorporating WebSockets for instantaneous lead updates and in-app messaging, agents can respond to customers in seconds. Interactive dashboard widgets break down sales metrics, conversation durations, and pipeline status dynamically.',
                'benefits': [
                    'Enables instantaneous client tracking to maximize sales pipeline velocity.',
                    'Reduces client support queue waiting times automatically.'
                ],
                'results': [
                    'Increased overall sales conversions by 18x through lead response automation.',
                    'Reduced support ticket queue times by 40% using priority queuing logic.'
                ]
            },
            {
                'title': 'Moto Bee Garage System',
                'category': 'custom',
                'desc': 'Custom software for garage owners featuring a real-time parts inventory dashboard and mobile app for mechanics.',
                'metric': '< 5s',
                'metricLabel': 'Dispatch Latency',
                'icon': 'FolderGit',
                'tech': ['Flutter', 'Go', 'Firebase', 'Polynexus Edge'],
                'image': 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&q=80&w=400&h=250',
                'file': 'motobee-inventory-sync.sh',
                'longDesc': 'The Moto Bee Garage System empowers auto repair shops with modern resource and inventory control. Mechanics use a custom mobile application to claim jobs, scan auto parts barcodes, and record service notes, while garage managers oversee operations, staff capacity, and parts catalog values from a comprehensive desktop dashboard.',
                'benefits': [
                    'Enables instant parts inventory synchronization to speed up repairs.',
                    'Provides a durable mobile application optimized for mechanic service bays.'
                ],
                'results': [
                    'Reduced parts dispatch and order matching times to under 5 seconds.',
                    'Increased mechanic utilization and bay turnover rates by 30%.'
                ]
            },
            {
                'title': 'Campus Flow',
                'category': 'polynexus',
                'desc': 'College & School management system managing member directory, student/teacher attendance, lecture schedules, and grading.',
                'metric': '99.8%',
                'metricLabel': 'Attendance Accuracy',
                'icon': 'Globe',
                'tech': ['Django', 'React', 'PostgreSQL', 'Tailwind CSS', 'Docker'],
                'image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&q=80&w=400&h=250',
                'file': 'campus-flow-directory.sh',
                'longDesc': 'Campus Flow is a comprehensive management platform designed for universities and schools. It unifies high-capacity student registries with automated staff attendance verification, daily lecture timetabling, and direct communication relays. By building a fast edge-indexed registry database, administrative workloads and student query latencies have been significantly minimized.',
                'benefits': [
                    'Simplifies school operations by consolidating student, staff, and lecture data.',
                    'Maintains precise daily attendance records with automated reports.',
                    'Provides real-time schedule relays for smooth academic course tracking.'
                ],
                'results': [
                    'Improved administrative staff productivity by 40%.',
                    'Achieved 99.8% attendance recording accuracy and reduced reporting latency.'
                ]
            }
        ]

        for p in projects_data:
            # Generate sample pricing tables for logistics/CRMs/Enterprise projects
            sample_table_html = """<div class="max-w-4xl mx-auto my-4">
  <div class="grid grid-cols-1 md:grid-cols-3 gap-0 border border-slate-200 rounded-3xl overflow-hidden shadow-xs bg-white">
    
    <!-- Basic Tier -->
    <div class="p-6 text-center flex flex-col justify-between border-b md:border-b-0 md:border-r border-slate-100 hover:bg-slate-50/50 transition-colors duration-200">
      <div>
        <span class="text-[10px] font-bold text-slate-450 uppercase tracking-widest block mb-4 font-sans">Basic</span>
        <div class="text-3xl font-extrabold text-slate-900 mb-6 font-mono select-all">$ 29</div>
        <ul class="space-y-3.5 text-xs text-slate-500 mb-6 font-sans">
          <li>1 full user</li>
          <li>1,000 Email Previews</li>
          <li>5 contacts per client</li>
          <li>5 coffee cups</li>
        </ul>
      </div>
      <button class="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-[10px] py-2.5 rounded-xl uppercase tracking-wider transition-colors duration-200 cursor-pointer">
        Buy Now
      </button>
    </div>

    <!-- Standard Tier -->
    <div class="p-6 text-center flex flex-col justify-between bg-slate-50 border-b md:border-b-0 md:border-r border-slate-100 hover:bg-slate-100/50 transition-colors duration-200">
      <div>
        <span class="text-[10px] font-bold text-slate-450 uppercase tracking-widest block mb-4 font-sans">Standard</span>
        <div class="text-3xl font-extrabold text-slate-900 mb-6 font-mono select-all">$ 59</div>
        <ul class="space-y-3.5 text-xs text-slate-550 mb-6 font-sans">
          <li>10 full user</li>
          <li>2,000 Email Previews</li>
          <li>10 contacts per client</li>
          <li>10 coffee cups</li>
        </ul>
      </div>
      <button class="w-full bg-[#3b82f6] hover:bg-[#2563eb] text-white font-bold text-[10px] py-2.5 rounded-xl uppercase tracking-wider transition-colors duration-200 cursor-pointer shadow-xs shadow-blue-500/10">
        Buy Now
      </button>
    </div>

    <!-- Advanced Tier -->
    <div class="p-6 text-center flex flex-col justify-between hover:bg-slate-50/50 transition-colors duration-200">
      <div>
        <span class="text-[10px] font-bold text-slate-450 uppercase tracking-widest block mb-4 font-sans">Advanced</span>
        <div class="text-3xl font-extrabold text-slate-900 mb-6 font-mono select-all">$ 99</div>
        <ul class="space-y-3.5 text-xs text-slate-500 mb-6 font-sans">
          <li>20 full user</li>
          <li>Unlimited Email Previews</li>
          <li>Unlimited contacts per client</li>
          <li>100 coffee cups</li>
        </ul>
      </div>
      <button class="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-[10px] py-2.5 rounded-xl uppercase tracking-wider transition-colors duration-200 cursor-pointer">
        Buy Now
      </button>
    </div>

  </div>
</div>"""
            
            # Map logical pricing according to project category
            project_price = "Starting from ₹199 / user / month"
            if "Mail" in p['title']:
                project_price = "Starting from ₹599 / unit / month"
            elif "ERP" in p['title']:
                project_price = "Starting from ₹999 / enterprise / month"
            elif "CRM" in p['title']:
                project_price = "Starting from ₹799 / user / month"
            elif "Garage" in p['title']:
                project_price = "Starting from ₹299 / employee / month"

            # If the category is polynexus, add the new pricing fields
            std_price = ''
            std_orig = ''
            prem_price = ''
            prem_orig = ''
            std_feats = []
            prem_feats = []
            ent_feats = []

            if p['category'] == 'polynexus':
                std_price = '1249'
                std_orig = '1499'
                prem_price = '2999'
                prem_orig = '3499'
                std_feats = [
                    'Create quotes and GST compliant invoices',
                    'Customize for local languages and tax laws',
                    'Multi-user access for up to 3 users',
                    'Handle multi-currency transactions',
                    'Set up automated payment reminders',
                    'Manage projects & timesheets',
                    'Enable self-service customer portal',
                    'Customize your transaction templates'
                ]
                prem_feats = [
                    'Includes everything in Standard +',
                    'Manage subscription billing',
                    'Multi-user access for up to 10 users',
                    'Use hosted payment pages',
                    'Automate billing for usage-based pricing models',
                    'Manage in-app purchases'
                ]
                ent_feats = [
                    'Helps enterprises handle',
                    'High volume customers and transactions',
                    'Advanced usage-based billing controls',
                    'Flexible revenue recognition configurations',
                    'Analytics with forecasting and AI insights',
                    'In-depth customization for reports and modules',
                    'Priority support and dedicated account manager'
                ]

            Project.objects.update_or_create(
                title=p['title'],
                defaults={
                    'category': p['category'],
                    'desc': p['desc'],
                    'metric': p['metric'],
                    'metricLabel': p['metricLabel'],
                    'icon': p['icon'],
                    'tech': p['tech'],
                    'image': p['image'],
                    'file': p['file'],
                    'longDesc': p.get('longDesc', ''),
                    'benefits': p.get('benefits', []),
                    'results': p.get('results', []),
                    'price': project_price,
                    'price_detail_html': sample_table_html,
                    'standard_price': std_price,
                    'standard_original_price': std_orig,
                    'premium_price': prem_price,
                    'premium_original_price': prem_orig,
                    'standard_features': std_feats,
                    'premium_features': prem_feats,
                    'enterprise_features': ent_feats
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(projects_data)} projects.'))

        # 3. Seed Testimonial Data
        testimonials_data = [
            {
                'name': 'Sarah Jenkins',
                'role': 'VP of Platform Engineering',
                'company': 'NovusAI',
                'content': 'Migrating our ingestion layers to Polynexus Serverless Edge reduced our global api latency from 180ms to under 12ms. Our devops team now spends close to zero hours debugging regional sync failures.',
                'rating': 5,
                'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=120&h=120'
            },
            {
                'name': 'David Chen',
                'role': 'Core Architect',
                'company': 'FlowState',
                'content': 'The Polymorphic Storage engine is exactly what modern startups need. We can link relations and document formats in a single Postgres-compatible interface, cutting down infrastructure bills by 40%.',
                'rating': 5,
                'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=120&h=120'
            },
            {
                'name': 'Elena Rostova',
                'role': 'Head of Security & Trust',
                'company': 'Securitas Cryptographic',
                'content': 'Polynexus Zero-Trust Shielding made SOC2 auditing a breeze. The out-of-the-box hardware key validations and encryption patterns are designed with rigorous, premium standards.',
                'rating': 5,
                'avatar': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=120&h=120'
            }
        ]

        for t in testimonials_data:
            Testimonial.objects.update_or_create(
                name=t['name'],
                defaults={
                    'role': t['role'],
                    'company': t['company'],
                    'content': t['content'],
                    'rating': t['rating'],
                    'avatar': t['avatar']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(testimonials_data)} testimonials.'))

        # 4. Seed FAQ Data
        faqs_data = [
            {
                'question': 'How does Polynexus achieve sub-2ms start times?',
                'answer': 'We leverage lightweight WebAssembly (WASM) isolates instead of full Docker containers or Node VM environments. This eliminates cold start overhead by executing routines in pre-allocated sandbox boundaries inside our global V8 edge cluster.'
            },
            {
                'question': 'Is Polymorphic Storage compatible with Postgres clients?',
                'answer': 'Yes! Polynexus utilizes a Postgres-wire protocol gateway. You can use standard client wrappers, ORMs, and drivers (like pg, Prisma, or Sequelize) while benefiting from our dynamic NoSQL schema capabilities on the server.'
            },
            {
                'question': 'Can I self-host the Polynexus grid orchestrator?',
                'answer': 'Absolutely. We support local and private-cloud orchestrator installations. You can link your proprietary clusters directly to the Polynexus routing bridge to leverage our AI dispatcher while keeping all data on-premise.'
            },
            {
                'question': 'How does the pricing scale for high-traffic apps?',
                'answer': 'We offer a serverless pay-as-you-go tier based on CPU runtime milliseconds and active write logs. For enterprise scaling, we provide fixed node capacities that deliver up to 60% compute discount thresholds.'
            }
        ]

        for f in faqs_data:
            FAQ.objects.update_or_create(
                question=f['question'],
                defaults={
                    'answer': f['answer']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(faqs_data)} FAQs.'))

        # 5. Seed BlogPost Data
        blog_posts_data = [
            {
                'title': 'Compiling Rust to WebAssembly for Sub-Millisecond APIs',
                'category': 'Engineering',
                'date': datetime.date(2026, 6, 18),
                'readTime': '6 min read',
                'summary': 'Learn the exact pipeline configuration we use to pre-compile and distribute rust-based WASM modules across edge clusters.',
                'imageUrl': 'https://images.unsplash.com/photo-1607799279861-4dd421887fb3?auto=format&fit=crop&q=80&w=400&h=250'
            },
            {
                'title': 'Architecting Polymorphic Databases: Relational vs Document',
                'category': 'Data Science',
                'date': datetime.date(2026, 5, 24),
                'readTime': '9 min read',
                'summary': 'An in-depth review of transaction locking schemas when handling graph relationships and JSON structures concurrently.',
                'imageUrl': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?auto=format&fit=crop&q=80&w=400&h=250'
            },
            {
                'title': 'How AI-Driven Network Routing Minimizes Power Costs',
                'category': 'Research',
                'date': datetime.date(2026, 4, 10),
                'readTime': '12 min read',
                'summary': 'Exploring reinforcement learning dispatcher policies that redirect transactional traffic into renewable-powered servers.',
                'imageUrl': 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=400&h=250'
            }
        ]

        for b in blog_posts_data:
            BlogPost.objects.update_or_create(
                title=b['title'],
                defaults={
                    'category': b['category'],
                    'date': b['date'],
                    'readTime': b['readTime'],
                    'summary': b['summary'],
                    'imageUrl': b['imageUrl']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(blog_posts_data)} blog posts.'))

        # 6. Seed Contact Settings
        ContactSetting.objects.update_or_create(
            pk=1,
            defaults={
                'email': 'info@polynexus.com',
                'phone': '+91 9226318818',
                'address': 'Nagpur, Maharashtra',
                'est_response': 'EST RESPONSE TIME: < 15 MINUTES'
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Contact Settings.'))

        # 7. Seed Hero Settings
        HeroSetting.objects.update_or_create(
            pk=1,
            defaults={
                'badge': 'CO-CREATING DIGITAL EXCELLENCE',
                'title_prefix': 'Building ',
                'title_highlight': 'custom software',
                'title_suffix': ' to maximize your business impact',
                'subtitle': 'We deeply understand your unique operational bottlenecks and design tailored engineering pathways to solve them. Skip rigid, off-the-shelf limitations and scale with bespoke solutions built strictly around your users, your workflows, and your long-term goals.',
                'cta1_text': 'Get Your Custom Solution',
                'cta1_link': '#contact',
                'cta2_text': 'View Our Services',
                'cta2_link': '#services',
                'trust_indicators': [
                    {"label": "Core Team", "value": "100% Expert Led", "icon": "Sparkles", "color": "text-secondary"},
                    {"label": "Performance", "value": "1.2ms Latency", "icon": "Zap", "color": "text-[#E27000]"},
                    {"label": "Availability", "value": "99.99% SLA", "icon": "Activity", "color": "text-purple-500"}
                ]
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded Hero Settings.'))
        self.stdout.write(self.style.SUCCESS('All dummy database data seeded successfully!'))
