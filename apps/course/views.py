from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from course.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from course.models import CourseResourse
from operation.models import UserFavorite, CourseComments


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,2 , request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses":courses,
            'sort': sort,
            'hot_courses':hot_courses,

        })


class CourseDetailView(View):
    '''课程详情'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        # 课程标签
        # 通过当前标签，查找数据库中的课程
        has_fav_course = False
        has_fav_org = False

        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, "course-detail.html", {
            'course': course,
            'relate_courses':relate_courses
        })


class CourseInfoView(View):
    '''课程章节信息'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResourse.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            'all_resources':all_resources
        })


class CommentsView(View):
    '''课程评论'''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResourse.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            'all_comments':all_comments,
        })


class AddCommentsView(View):
    '''用户评论'''
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            # 实例化一个course_comments对象
            course_comments = CourseComments()
            # 获取评论的是哪门课程
            course = Course.objects.get(id = int(course_id))
            # 分别把评论的课程、评论的内容和评论的用户保存到数据库
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')