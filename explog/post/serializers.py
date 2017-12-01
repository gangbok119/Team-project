from rest_framework import serializers

from .models import Post, PostReply, PostText, PostPath, PostPhoto, PostContent


class PostSerializer(serializers.ModelSerializer):
    # User 정보를 author에 표현하기 위해 멤버 모델 완성 후 바꿔줘야함
    #author = UserSerializer()

    class Meta:
        model = Post
        fields =(
            'pk',
            'author',
            'title',
            'start_date',
            'end_date',
            'created_at',


        )

# PostList 뷰에서 Post의 첫 번째 사진을 보여주기위한 시리얼라이저
class PostListSerializer(serializers.ModelSerializer):
    # User 정보를 author에 표현하기 위해 멤버 모델 완성 후 바꿔줘야함
    #author = UserSerializer()

    # PostList뷰에서 Post의 첫 사진을 커버로 이용하기 위한 필드
    # method필드가 아니라 릴레이션필드를 사용해야함.
    photo = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields =(
            'pk',
            'author',
            'title',
            'start_date',
            'end_date',
            'created_at',
            'photo',

        )

    # 메소드필드에 필요한 데이터를 넣는 법
    # get_필드이름
    def get_photo(self,obj):
        #post의 pk를 받음
        obj_pk = obj.pk
        #post의 pk를 이용하여 필요한 객체를 얻음
        photo_qs = PostPhoto.objects.filter(post=obj_pk).first()
        #photo 데이터 직렬화 - 한 개의 데이터는 many=False
        photo = PostPhotoSerializer(photo_qs, many=False).data
        return photo


class PostReplySerializer(serializers.ModelSerializer):
    # User 정보를 author에 표현하기 위해 멤버 모델 완성 후 바꿔줘야함
    # author = UserSerializer()
    class Meta:
        model = PostReply
        fields = (
            'pk',
            'post',
            'author',
            'content',
            'created_at',
        )

class PostTextSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostText
        fields = (
            'pk',
            'title',
            'content',
            'created_at',
            'post',

        )


class PostPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostPhoto
        fields =(
            'pk',
            'photo',
            'created_at',
            'content_group',
        )


class PostItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostContent
        fields = (
            'pk',
            'post',

        )
# PostPhoto 객체를 여러 개 받기 위한 시리얼라이저
# 강사님께 트러블슈팅 요망
class PhotoListSerializer ( serializers.Serializer ) :
    photo = serializers.ListField(
                        # PostPhoto를 Image필드로 주었는데 여기서 Image필드인지 File필드인지 확인 필요
                       child=serializers.FileField( max_length=100000,
                                         allow_empty_file=False,
                                         use_url=False )
                                )
    def create(self, validated_data):
        content_group=PostContent.objects.latest('created_at')
        photo=validated_data.pop('photo')
        for img in photo:
            photo=PostPhoto.objects.create(photo=img,content_group=content_group,**validated_data)
        return photo


class PostPathSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostPath
        fields = (
            'pk',
            'lat',
            'lng',
            'post',

        )


class PostDetailSerializer(serializers.ModelSerializer):
    # User 정보를 author에 표현하기 위해 멤버 모델 완성 후 바꿔줘야함
    #author = UserSerializer()

    #post detail에서 관련 내용들을 전부 가져오기 위한 메서드필드
    text = serializers.StringRelatedField()
    photo = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    reply = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields =(
            'pk',
            'author',
            'title',
            'start_date',
            'end_date',
            'created_at',
            'text',
            'photo',
            'path',
            'reply',
        )


    def get_photo(self,obj):
        obj_pk = obj.pk
        photo_qs = PostText.objects.filter(post=obj_pk)
        photo = PostTextSerializer(photo_qs,many=True).data
        return photo
    def get_path(self,obj):
        obj_pk = obj.pk
        path_qs = PostText.objects.filter(post=obj_pk)
        path = PostTextSerializer(path_qs,many=True).data
        return path

    #역참조 postreply.set relationfield
    def get_reply(self,obj):
        obj_pk = obj.pk
        reply_qs = PostReply.objects.filter(post=obj_pk)
        reply = PostReplySerializer(reply_qs,many=True).data
        return reply