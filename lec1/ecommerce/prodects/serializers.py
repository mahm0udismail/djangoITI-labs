from rest_framework import serializers
from .models import Category, Producer, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested serializer
    producers = ProducerSerializer(many=True)  # List of producers

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'category', 'producers']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        producers_data = validated_data.pop('producers')

        category, _ = Category.objects.get_or_create(**category_data)
        product = Product.objects.create(category=category, **validated_data)

        for producer_data in producers_data:
            producer, _ = Producer.objects.get_or_create(**producer_data)
            product.producers.add(producer)

        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        producers_data = validated_data.pop('producers', None)

        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category

        if producers_data:
            instance.producers.clear()
            for producer_data in producers_data:
                producer, _ = Producer.objects.get_or_create(**producer_data)
                instance.producers.add(producer)

        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        
        return instance
