// Fill out your copyright notice in the Description page of Project Settings.


#include "KM_GAActor.h"

FName AKM_GAActor::AbilitySystemComponentName(TEXT("AbilitySystemComponent0"));

// Sets default values
AKM_GAActor::AKM_GAActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	AbilitySystemComponent = CreateOptionalDefaultSubobject<UAbilitySystemComponent>(AKM_GAActor::AbilitySystemComponentName);
}

// Called when the game starts or when spawned
void AKM_GAActor::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AKM_GAActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

