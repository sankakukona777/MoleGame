// Fill out your copyright notice in the Description page of Project Settings.


#include "KM_GACharacter.h"

FName AKM_GACharacter::AbilitySystemComponentName(TEXT("AbilitySystemComponent0"));

// Sets default values
AKM_GACharacter::AKM_GACharacter()
{
 	// Set this character to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	AbilitySystemComponent = CreateOptionalDefaultSubobject<UAbilitySystemComponent>(AKM_GACharacter::AbilitySystemComponentName);
}

// Called when the game starts or when spawned
void AKM_GACharacter::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AKM_GACharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

// Called to bind functionality to input
void AKM_GACharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

}

