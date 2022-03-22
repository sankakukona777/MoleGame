// Fill out your copyright notice in the Description page of Project Settings.


#include "KM_GAPawn.h"

FName AKM_GAPawn::AbilitySystemComponentName(TEXT("AbilitySystemComponent0"));

// Sets default values
AKM_GAPawn::AKM_GAPawn()
{
 	// Set this pawn to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	AbilitySystemComponent = CreateOptionalDefaultSubobject<UAbilitySystemComponent>(AKM_GAPawn::AbilitySystemComponentName);
}

// Called when the game starts or when spawned
void AKM_GAPawn::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AKM_GAPawn::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

// Called to bind functionality to input
void AKM_GAPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

}

